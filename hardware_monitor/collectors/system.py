import random

def get_system_data(hostname=None):
    """
    Returns a dictionary with system info, RAM, Disk, and peripherals.
    Hostname argument is optional for dummy data.
    """
    ram_total = random.choice([8, 16, 32, 64])
    ram_used = round(random.uniform(1, ram_total), 1)
    ram_usage = round((ram_used / ram_total) * 100, 1)

    disk_size = random.choice([256, 512, 1024, 2048])
    disk_used = round(random.uniform(0.1, disk_size), 1)
    disk_free = disk_size - disk_used
    disk_usage = round((disk_used / disk_size) * 100, 1)

    monitors = [("Dell", "U2419H"), ("LG", "27UK850"), ("Samsung", "S24R650")]
    mice = [("Logitech", "MX Master 3"), ("Razer", "DeathAdder"), ("Microsoft", "IntelliMouse")]
    keyboards = [("Logitech", "K380"), ("Corsair", "K70"), ("Microsoft", "Ergonomic")]

    monitor = random.choice(monitors)
    mouse = random.choice(mice)
    keyboard = random.choice(keyboards)

    return {
        "hostname": hostname or f"host_{random.randint(1,100)}",
        "ip_address": f"192.168.{random.randint(0,255)}.{random.randint(1,254)}",
        "logged_user": random.choice(["alice", "bob", "carol", "dave"]),
        "ram_total_gb": ram_total,
        "ram_used_gb": ram_used,
        "ram_usage_pct": ram_usage,
        "disk_name": random.choice(["sda", "sdb", "nvme0n1"]),
        "disk_size_gb": disk_size,
        "disk_total_gb": disk_size,
        "disk_used_gb": disk_used,
        "disk_free_gb": disk_free,
        "disk_usage_pct": disk_usage,
        "monitor_vendor": monitor[0],
        "monitor_model": monitor[1],
        "mouse_vendor": mouse[0],
        "mouse_model": mouse[1],
        "keyboard_vendor": keyboard[0],
        "keyboard_model": keyboard[1],
    }
