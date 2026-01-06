import random

def get_cpu_data(hostname=None):
    """
    Returns a dictionary with CPU data.
    Hostname argument is ignored for dummy data.
    """
    return {
        "cpu_model": random.choice(["Intel i5-10400", "Intel i7-10700", "AMD Ryzen 5 3600", "AMD Ryzen 7 3700X"]),
        "cpu_temperature": round(random.uniform(30, 85), 1),
        "cpu_core": random.choice([4, 6, 8]),
        "cpu_thread": random.choice([8, 12, 16]),
        "cpu_clockspeed": round(random.uniform(2.0, 4.0), 2),
        "cpu_utilization_pct": round(random.uniform(5, 95), 1)
    }
