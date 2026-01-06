import psutil  
from common_resources import log_error as _log_error
import subprocess


class Utilize:
    """Class to capture utilization of RAM, Storage and CPU.
    """

    def __init__(self): 
        """Initialzing class.
        """
        pass
        

    def update_cpu(self): 
        """Retrieve cpu utilization in percentage.

        Returns:
            (float): 
        """
        cpu_percent = float(psutil.cpu_percent(interval=1))

        return {
            "cpu_percent": cpu_percent,
        }


    def update_ram(self):
        """Retrieve total ram usage from all mounted RAM devices.

        Returns:
            (float): _description_
        """
        ram = psutil.virtual_memory()
        ram_total_gb = float(round(ram.total / (1024**3), 2))
        ram_used_gb = float(round(ram.used / (1024**3), 2))
        ram_usage_percent = float(ram.percent)
        
        
        return {
            "ram_total_gb": ram_total_gb,
            "ram_used_gb": ram_used_gb,
            "ram_usage_percent": ram_usage_percent
        }


    def update_disk(self):
        # rewrite better.
        """
        Retrieve total disk usage from all mounted storage devices.

        Uses df -h to get human-readable disk stats (G, M, T) and extracts:
        - total disk size
        - used space
        - free space
        - usage percentage

        Only keeps values in gigabytes (GB) and converts them to floats.

        Returns:
            dict: {
                "disk_total_gb": float,
                "disk_used_gb": float,
                "disk_free_gb": float,
                "disk_usage_percent": float
            }
        
        Raises:
            RuntimeError: If df command fails.
            ValueError: If output is incomplete or cannot be converted.

        """

        result = subprocess.run("df -h --total -x tmpfs -x devtmpfs -x squashfs -x overlay | grep ^total", shell=True, capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout.strip():
            raise RuntimeError("Failed to retrieve disk usage info")
        
        parts = result.stdout.split()
        if len(parts) < 5:
            raise ValueError(f"Unexpected df output format: {result.stdout}")
        

        disk_total = parts[1]
        disk_used = parts[2]
        disk_free = parts[3]
        disk_usage = parts[4]

        def to_gb(value):
             """
             Convert disk size values like '200G', '1.5T', '800M' into gigabytes (GB).
             """
             if value.endswith("G"):
                 return float(value.replace("G", ""))

             if value.endswith("T"):
                 return float(value.replace("T", "")) * 1024.0  # 1 TB = 1024 GB

             if value.endswith("M"):
                 return float(value.replace("M", "")) / 1024.0  # 1 GB = 1024 MB

             raise ValueError(f"Unknown disk unit in value: {value}")
        try:
            disk_all = {
                    "disk_total_gb" : to_gb(disk_total),
                    "disk_used_gb" : to_gb(disk_used),
                    "disk_free_gb" : to_gb(disk_free),
                    "disk_usage_percent" : float(disk_usage.rstrip("%"))
            }

        except ValueError: 
            _log_error("Disk conversion failed", parts)
            return {}
        
        return disk_all

    def update_all(self):
        cpu_info = self.update_cpu()
        ram_info = self.update_ram()
        disk_info = self.update_disk()
        print("update all has run")

        return {
            "cpu": cpu_info,
            "ram": ram_info,
            "disk": disk_info
        }


if __name__ == "__main__":
    pc = Utilize()
    disk_data = pc.update_disk()   
    print(disk_data)               
    print(type(disk_data))         



