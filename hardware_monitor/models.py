from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class SystemInventory(db.Model):
    __tablename__ = "sys_info"



    __table_args__ = (
    db.Index("idx_host_timestamp", "hostname", "timestamp"),
)




    #  Primary Key
    id = db.Column(db.Integer, primary_key=True)

    #  Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #  System Info
    hostname = db.Column(db.String(100), index=True)
    ip_address = db.Column(db.String(50))
    logged_user = db.Column(db.String(100))

    #  CPU Info
    cpu_model = db.Column(db.String(150))
    cpu_temperature = db.Column(db.Float)
    cpu_core = db.Column(db.Integer)
    cpu_thread = db.Column(db.Integer)
    cpu_clockspeed = db.Column(db.Float)
    cpu_utilization_pct = db.Column(db.Float)

    #  RAM Info
    ram_total_gb = db.Column(db.Float)
    ram_usage_pct = db.Column(db.Float)
    ram_used_gb = db.Column(db.Float)

    #  Disk Info
    disk_name = db.Column(db.String(100))
    disk_size_gb = db.Column(db.Float)
    disk_total_gb = db.Column(db.Float)
    disk_used_gb = db.Column(db.Float)
    disk_free_gb = db.Column(db.Float)
    disk_usage_pct = db.Column(db.Float)

    #  Monitor Info
    monitor_vendor = db.Column(db.String(100))
    monitor_model = db.Column(db.String(100))

    #  Mouse Info
    mouse_vendor = db.Column(db.String(100))
    mouse_model = db.Column(db.String(100))

    #  Keyboard Info
    keyboard_vendor = db.Column(db.String(100))
    keyboard_model = db.Column(db.String(100))

    def __repr__(self):
        return f"<SystemInventory {self.hostname} @ {self.timestamp}>"







# real system data


# import socket
# import psutil
# import platform
# from datetime import datetime

# def collect_system_inventory():
#     hostname = socket.gethostname()
#     ip_address = socket.gethostbyname(hostname)

#     cpu_freq = psutil.cpu_freq()
#     vm = psutil.virtual_memory()
#     disk = psutil.disk_usage("/")

#     record = SystemInventory(
#         timestamp=datetime.utcnow(),

#         hostname=hostname,
#         ip_address=ip_address,
#         logged_user=psutil.users()[0].name if psutil.users() else None,

#         cpu_model=platform.processor(),
#         cpu_temperature=None,  # OS / hardware dependent
#         cpu_core=psutil.cpu_count(logical=False),
#         cpu_thread=psutil.cpu_count(logical=True),
#         cpu_clockspeed=cpu_freq.current if cpu_freq else None,
#         cpu_utilization_pct=psutil.cpu_percent(interval=1),

#         ram_total_gb=round(vm.total / (1024**3), 2),
#         ram_used_gb=round(vm.used / (1024**3), 2),
#         ram_usage_pct=vm.percent,

#         disk_name="/",
#         disk_size_gb=round(disk.total / (1024**3), 2),
#         disk_total_gb=round(disk.total / (1024**3), 2),
#         disk_used_gb=round(disk.used / (1024**3), 2),
#         disk_free_gb=round(disk.free / (1024**3), 2),
#         disk_usage_pct=disk.percent,

#         monitor_vendor=None,
#         monitor_model=None,
#         mouse_vendor=None,
#         mouse_model=None,
#         keyboard_vendor=None,
#         keyboard_model=None,
#     )

#     db.session.add(record)
#     db.session.commit()
