import csv
import random
from datetime import datetime, timedelta

csv_file = "dummy_system_data.csv"

hostnames = [f"host{i}" for i in range(1, 11)]
users = ["alice", "bob", "carol", "dave", "eve", "frank", "grace", "heidi", "ivan", "judy"]
cpu_models = ["Intel i5-10400", "Intel i7-10700", "AMD Ryzen 5 3600", "AMD Ryzen 7 3700X"]
disk_names = ["sda", "sdb", "nvme0n1"]
monitors = [("Dell", "U2419H"), ("LG", "27UK850"), ("Samsung", "S24R650")]
mice = [("Logitech", "MX Master 3"), ("Razer", "DeathAdder"), ("Microsoft", "IntelliMouse")]
keyboards = [("Logitech", "K380"), ("Corsair", "K70"), ("Microsoft", "Ergonomic")]

start_date = datetime(2025, 11, 1, 0, 0)
interval = timedelta(minutes=15)
num_days = 30
rows_per_host = num_days * 24 * 4  # 15-min intervals per host

fieldnames = [
    "timestamp",
    "hostname",
    "ip_address",
    "logged_user",

    "cpu_model",
    "cpu_temperature",
    "cpu_core",
    "cpu_thread",
    "cpu_clockspeed",
    "cpu_utilization_pct",

    "ram_total_gb",
    "ram_usage_pct",
    "ram_used_gb",

    "disk_name",
    "disk_size_gb",
    "disk_total_gb",
    "disk_used_gb",
    "disk_free_gb",
    "disk_usage_pct",

    "monitor_vendor",
    "monitor_model",

    "mouse_vendor",
    "mouse_model",

    "keyboard_vendor",
    "keyboard_model"
]


with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for hostname in hostnames:
        current_time = start_date
        for _ in range(rows_per_host):
            cpu_temp = round(random.uniform(30, 85), 1)
            cpu_util = round(random.uniform(5, 95), 1)
            ram_total = random.choice([8, 16, 32, 64])
            ram_used_gb = round(random.uniform(1, ram_total), 1)
            ram_usage = round((ram_used_gb / ram_total) * 100, 1)
            disk_size = random.choice([256, 512, 1024, 2048])
            disk_used = round(random.uniform(0.1, disk_size), 1)
            disk_free = disk_size - disk_used
            disk_usage = round((disk_used / disk_size) * 100, 1)
            
        writer.writerow({
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "hostname": hostname,
                "ip_address": f"192.168.{random.randint(0,255)}.{random.randint(1,254)}",
                "logged_user": random.choice(users),
            
                "cpu_model": random.choice(cpu_models),
                "cpu_temperature": cpu_temp,
                "cpu_core": random.choice([4, 6, 8]),
                "cpu_thread": random.choice([8, 12, 16]),
                "cpu_clockspeed": round(random.uniform(2.0, 4.0), 2),
                "cpu_utilization_pct": cpu_util,
            
                "ram_total_gb": ram_total,
                "ram_usage_pct": ram_usage,
                "ram_used_gb": ram_used_gb,
            
                "disk_name": random.choice(disk_names),
                "disk_size_gb": disk_size,
                "disk_total_gb": disk_size,
                "disk_used_gb": disk_used,
                "disk_free_gb": disk_free,
                "disk_usage_pct": disk_usage,
            
                "monitor_vendor": random.choice(monitors)[0],
                "monitor_model": random.choice(monitors)[1],
            
                "mouse_vendor": random.choice(mice)[0],
                "mouse_model": random.choice(mice)[1],
            
                "keyboard_vendor": random.choice(keyboards)[0],
                "keyboard_model": random.choice(keyboards)[1],
            })
            
        current_time += interval

print(f"Dummy system CSV generated: {csv_file}")





