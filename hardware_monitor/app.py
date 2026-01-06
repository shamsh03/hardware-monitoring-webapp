from flask import Flask, render_template, jsonify
from config import Config
from sqlalchemy import func
from models import db, SystemInventory
from services.data_service import collect_and_store
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from threading import Lock
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

scheduler = None

COLLECTION_ENABLED = False
toggle_lock = Lock()

# ------------- Helper for safe rounding ----------------
def safe_round(val):
    return round(val) if val is not None else 0

# ---------------- API Routes --------------------------

@app.route("/api/data")
def api_data():
    rows = (
        SystemInventory.query
        .order_by(SystemInventory.timestamp.desc())
        .all()
    )

    return jsonify([
        {
           "Timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "Hostname": r.hostname,
            "CPU Utilization(%)": r.cpu_utilization_pct,
            "RAM_Usage(%)": r.ram_usage_pct,
            "Disk_Usage(%)": r.disk_usage_pct,

            "Monitor Vendor": r.monitor_vendor,
            "Monitor Model": r.monitor_model,

            "Mouse Vendor": r.mouse_vendor,
            "Mouse Model": r.mouse_model,

            "Keyboard Vendor": r.keyboard_vendor,
            "Keyboard Model": r.keyboard_model
        }
        for r in rows
    ])



@app.route("/api/table-latest")
def table_latest():
    subq = (
        db.session.query(
            SystemInventory.hostname,
            func.max(SystemInventory.timestamp).label("max_ts")
        )
        .group_by(SystemInventory.hostname)
        .subquery()
    )

    rows = (
        db.session.query(SystemInventory)
        .join(subq,
              (SystemInventory.hostname == subq.c.hostname) &
              (SystemInventory.timestamp == subq.c.max_ts))
        .all()
    )

    return jsonify([{
        "hostname": r.hostname,
        "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": safe_round(r.cpu_utilization_pct),
        "ram": safe_round(r.ram_usage_pct),
        "disk": safe_round(r.disk_usage_pct),
        "monitorVendor": r.monitor_vendor or "-",
        "monitorModel": r.monitor_model or "-",
        "mouseVendor": r.mouse_vendor or "-",
        "mouseModel": r.mouse_model or "-",
        "keyboardVendor": r.keyboard_vendor or "-",
        "keyboardModel": r.keyboard_model or "-"
    } for r in rows])

@app.route("/api/utilization/latest")
def utilization_latest():
    sub = (
        db.session.query(
            SystemInventory.hostname,
            func.max(SystemInventory.timestamp).label("max_time")
        )
        .group_by(SystemInventory.hostname)
        .subquery()
    )

    rows = (
        db.session.query(SystemInventory)
        .join(sub,
              (SystemInventory.hostname == sub.c.hostname) &
              (SystemInventory.timestamp == sub.c.max_time))
        .all()
    )

    return jsonify([
        {
            "Hostname": r.hostname,
            "Timestamp": r.timestamp.isoformat(),
            "CPU": safe_round(r.cpu_utilization_pct),
            "RAM": safe_round(r.ram_usage_pct),
            "Disk": safe_round(r.disk_usage_pct)
        }
        for r in rows
    ])


@app.route("/api/utilization/peripherals/<hostname>")
def utilization_peripherals(hostname):

    r = (
        SystemInventory.query
        .filter_by(hostname=hostname)
        .order_by(SystemInventory.timestamp.desc())
        .first()
    )

    if not r:
        return jsonify([])

    return jsonify([
        f"Monitor :- {r.monitor_vendor} | {r.monitor_model}",
        f"Mouse :- {r.mouse_vendor} | {r.mouse_model}",
        f"Keyboard :- {r.keyboard_vendor} | {r.keyboard_model}",
    ])



@app.route("/api/utilization/history/<hostname>")
def utilization_history(hostname):

    rows = (
        db.session.query(
            func.date(SystemInventory.timestamp).label("day"),
            func.max(SystemInventory.cpu_utilization_pct).label("cpu"),
            func.max(SystemInventory.ram_usage_pct).label("ram"),
            func.max(SystemInventory.disk_usage_pct).label("disk"),
        )
        .filter(SystemInventory.hostname == hostname)
        .group_by(func.date(SystemInventory.timestamp))
        .order_by(func.date(SystemInventory.timestamp))
        .all()
    )

    return jsonify({
        "labels": [r.day for r in rows],
        "cpu": [safe_round(r.cpu) for r in rows],
        "ram": [safe_round(r.ram) for r in rows],
        "disk": [safe_round(r.disk) for r in rows],
    })



# HOST DAILY HISTORY (FAST) for lg

@app.route("/api/host-history/<hostname>")
def host_history(hostname):

    rows = (
        db.session.query(
            func.date(SystemInventory.timestamp).label("day"),
            func.avg(SystemInventory.cpu_utilization_pct).label("cpu"),
            func.avg(SystemInventory.ram_usage_pct).label("ram"),
            func.avg(SystemInventory.disk_usage_pct).label("disk")
        )
        .filter(SystemInventory.hostname == hostname)
        .group_by(func.date(SystemInventory.timestamp))
        .order_by(func.date(SystemInventory.timestamp))
        .all()
    )

    return jsonify([{
        "day": r.day,
        "cpu": safe_round(r.cpu),
        "ram": safe_round(r.ram),
        "disk": safe_round(r.disk)
    } for r in rows])


# DASHBOARD SUMMARY :- Shows Top 10 Critical Systems

@app.route("/api/dashboard-summary") 
def dashboard_summary():

    # Subquery: latest timestamp per hostname 
    latest_subquery = ( 
    db.session.query( 
    		SystemInventory.hostname.label("hostname"),
            func.max(SystemInventory.timestamp).label("max_time") 
    	)
     	.group_by(SystemInventory.hostname) 
    	.subquery() 
    )
     # Main query joined with subquery 
    rows = ( 
    	db.session.query( 
    		SystemInventory.hostname.label("Hostname"), 				
            SystemInventory.timestamp.label("Timestamp"),
            SystemInventory.cpu_utilization_pct.label("cpu"),
            SystemInventory.ram_usage_pct.label("ram"),
            SystemInventory.disk_usage_pct.label("disk"), 
    )
     .join( 
    	latest_subquery, 
    	(SystemInventory.hostname == latest_subquery.c.hostname) & 
    	(SystemInventory.timestamp == latest_subquery.c.max_time) 
      ) 
      .all() 
    ) 
    # Convert ORM rows to dicts 
    result = [ 
          { 
    	"Hostname": r.Hostname, 
    	"Timestamp": r.Timestamp, 
    	"cpu": r.cpu, "ram": r.ram, 
    	"disk": r.disk 
          }
           for r in rows ] 
    

    # Top 10 high utilization 
    cpu = sorted([r for r in result if r["cpu"] >= 80], key=lambda x: 
    x["cpu"], reverse=True)[:10] 
    ram = sorted([r for r in result if r["ram"] >= 80], key=lambda x: 
    x["ram"], reverse=True)[:10] 
    disk = sorted([r for r in result if r["disk"] >= 80], key=lambda x: 
    x["disk"], reverse=True)[:10] 

    last_updated = max(r["Timestamp"] for r in result) if result else None 

    return jsonify({ 
    	"cpu": cpu, 
    	"ram": ram, 
    	"disk": disk, 
    	"lastUpdated": last_updated.isoformat() if last_updated else None 
}) 




@app.route("/api/collection/toggle", methods=["POST"])
def toggle_collection():
    global COLLECTION_ENABLED

    with toggle_lock:
        COLLECTION_ENABLED = not COLLECTION_ENABLED

    print("COLLECTION_ENABLED =", COLLECTION_ENABLED)

    return jsonify({
        "collectionEnabled": COLLECTION_ENABLED
    })




@app.route("/api/collection/status")
def collection_status():
    return jsonify({
        "collectionEnabled": COLLECTION_ENABLED
    })













# ---------------- Page Routes --------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/table")
def table():
    return render_template("table.html")

@app.route("/utilization")
def utilization():
    return render_template("utilization.html")

@app.route("/header.html")
def header():
    return render_template("header.html")

@app.route("/footer.html")
def footer():
    return render_template("footer.html")

# ---------------- Scheduler --------------------------


def start_scheduler():
    global scheduler

    if scheduler and scheduler.running:
        return

    scheduler = BackgroundScheduler(daemon=True)

    systems = [
        "host1","host2","host3","host4","host5","host6",
        "host7","host8","host9","host10","host11","host12"
    ]

    def scheduled_job():
        with toggle_lock:
            if not COLLECTION_ENABLED:
                print("Collection OFF — skipping")
                return

        with app.app_context():
            print("Collection ON — storing data")
            for host in systems:
                collect_and_store(hostname=host)

    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        minutes=1,
        id="data_collector",
        replace_existing=True
    )

    scheduler.start()




# ---------------- App Runner --------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    start_scheduler()
    app.run(debug=True, use_reloader=False)




