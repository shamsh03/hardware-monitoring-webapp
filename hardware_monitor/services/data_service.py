from datetime import datetime
from collectors.cpu import get_cpu_data
from collectors.system import get_system_data
from models import db, SystemInventory

def collect_and_store(hostname=None):
    """
    Collect system data for a specific host (or local if None) and store in DB.
    """
    data = {}

    # Use current timestamp
    data["timestamp"] = datetime.utcnow()

    # Collect system-specific data
    data.update(get_system_data(hostname))
    data.update(get_cpu_data(hostname))

    # Fill missing fields with defaults to avoid None issues
    data.setdefault("cpu_utilization_pct", 0)
    data.setdefault("ram_usage_pct", 0)
    data.setdefault("disk_usage_pct", 0)
    data.setdefault("hostname", hostname or "local")

    record = SystemInventory(**data)
    db.session.add(record)
    db.session.commit()
