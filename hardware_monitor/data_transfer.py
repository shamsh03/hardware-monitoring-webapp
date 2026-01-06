import csv
from datetime import datetime
from app import app
from models import db, SystemInventory

CSV_FILE = "/home/shamshs/Documents/work/Task6/hardware_monitor/dummy_system_data.csv"

def parse_float(val):
    return float(val) if val else None

def parse_int(val):
    return int(val) if val else None

def parse_datetime(val):
    return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")

with app.app_context():

    # 1. Fetch existing unique keys once
    existing_keys = {
        (r.hostname, r.timestamp)
        for r in db.session.query(
            SystemInventory.hostname,
            SystemInventory.timestamp
        ).all()
    }

    batch = []
    skipped = 0

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ts = parse_datetime(row["Timestamp"])
            host = row["Hostname"]

            # 2. Skip duplicates
            if (host, ts) in existing_keys:
                skipped += 1
                continue

            record = SystemInventory(
                timestamp=ts,
                hostname=host,
                ip_address=row["IP_Address"],
                logged_user=row["Logged_USER"],

                cpu_model=row["CPU_Model"],
                cpu_temperature=parse_float(row["CPU_Temperature"]),
                cpu_core=parse_int(row["CPU_Core"]),
                cpu_thread=parse_int(row["CPU_Thread"]),
                cpu_clockspeed=parse_float(row["CPU_ClockSpeed"]),
                cpu_utilization_pct=parse_float(row["CPU_Utilization_pct"]),

                ram_total_gb=parse_float(row["RAM_Total_GB"]),
                ram_usage_pct=parse_float(row["RAM_Usage_pct"]),
                ram_used_gb=parse_float(row["RAM_Used_GB"]),

                disk_name=row["Disk_Name"],
                disk_size_gb=parse_float(row["Disk_Size_GB"]),
                disk_total_gb=parse_float(row["Disk_Total_GB"]),
                disk_used_gb=parse_float(row["Disk_Used_GB"]),
                disk_free_gb=parse_float(row["Disk_Free_GB"]),
                disk_usage_pct=parse_float(row["Disk_Usage_pct"]),

                monitor_vendor=row["Monitor_Vendor"],
                monitor_model=row["Monitor_Model"],
                mouse_vendor=row["Mouse_Vendor"],
                mouse_model=row["Mouse_Model"],
                keyboard_vendor=row["Keyboard_Vendor"],
                keyboard_model=row["Keyboard_Model"],
            )

            batch.append(record)
            existing_keys.add((host, ts))  # prevents duplicates within same CSV

    # 3. Bulk insert
    if batch:
        db.session.bulk_save_objects(batch)
        db.session.commit()

    print(f"Inserted: {len(batch)}")
    print(f"Skipped (duplicates): {skipped}")
