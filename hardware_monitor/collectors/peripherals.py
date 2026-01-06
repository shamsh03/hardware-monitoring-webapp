import subprocess
import re

def get_peripherals_hwinfo():
    try:
        out = subprocess.check_output(
            ["hwinfo", "--monitor", "--keyboard", "--mouse"],
            stderr=subprocess.DEVNULL
        ).decode()

        monitor_vendor = monitor_model = None
        keyboard_vendor = keyboard_model = None
        mouse_vendor = mouse_model = None

        for block in out.split("\n\n"):
            if "Monitor" in block:
                vendor = re.search(r"Vendor:\s*(.*)", block)
                model = re.search(r"Model:\s*(.*)", block)
                monitor_vendor = vendor.group(1) if vendor else None
                monitor_model = model.group(1) if model else None

            if "Keyboard" in block:
                vendor = re.search(r"Vendor:\s*(.*)", block)
                model = re.search(r"Model:\s*(.*)", block)
                keyboard_vendor = vendor.group(1) if vendor else None
                keyboard_model = model.group(1) if model else None

            if "Mouse" in block:
                vendor = re.search(r"Vendor:\s*(.*)", block)
                model = re.search(r"Model:\s*(.*)", block)
                mouse_vendor = vendor.group(1) if vendor else None
                mouse_model = model.group(1) if model else None

        return (
            monitor_vendor, monitor_model,
            keyboard_vendor, keyboard_model,
            mouse_vendor, mouse_model
        )

    except Exception:
        return (None, None, None, None, None, None)
