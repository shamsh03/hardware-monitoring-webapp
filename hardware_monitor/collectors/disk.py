import subprocess
from common_resources import log_error as _log_error

class Disk:
    def __init__(self):
        """
        Class Disk Initialized. 
        """
        self.disks = self.name()
        

    def name(self):
        """
        Fetch all disk devices available on the system.
        Uses `lsblk` to list block devices and filters only disk-type entries.

        Returns:
            list[str]: A list of disk names (e.g., ["sda", "sdb"]).
        """

        try:
            result = subprocess.run(["lsblk","-dn", "-o", "NAME,TYPE"],
                         capture_output=True,text=True,check=True)
            lines = result.stdout.strip().split("\n")
            disks = [line.split()[0] for line in lines if "disk" in line]
            
        except Exception as e:
            _log_error ("Disk Name Failed",e)
            return ["Error Fetching Disk Name"]
        
        return disks if disks else []
        
    

    def size(self):
            """
            Retrieve the size of each disk in gigabytes (GB).

            Uses `lsblk` to fetch raw disk sizes and converts:
            - T (Terabytes) → GB (T * 1024)
            - G (Gigabytes) → GB (as is)
            - M (Megabytes) → GB (M / 1024)

            Returns:
                dict: { "sda": float(size), "sdb": float(size), ... }

            """

            sizes = {}
            try:
                result = subprocess.run(["lsblk", "-dn", "-o", "NAME,SIZE"],
                            capture_output=True,text=True,check=True)
                for line in result.stdout.strip().split("\n"):
                    parts = line.split()
                    if len(parts) == 2 and parts[0] in self.disks:
                        disk_name = parts[0]
                        size = parts[1]
                        numeric = ''.join(c for c in size if c.isdigit() or c == '.')
                        value = float(numeric) if numeric else 0.0
    
                        if 'T' in size:
                            value *= 1024
                        elif 'M' in size:
                            value /= 1024
    
                        sizes[disk_name] = round(value, 2)
                
                                   
            except Exception as e:
                _log_error ("Disk Size Failed",e)
                return ["Error Fetching Disk Size"]
            
            return sizes if sizes else []

             


    def serial_number (self):
        """
        Retrieve serial numbers for each disk device.

        Uses `lsblk` with the SERIAL column.
        If a disk has no serial number, returns 'N/A'.

        Returns:
            dict: { "sda": "ABCD1234", "sdb": "N/A", ... }

        """

        serials = {}
        try:
            result = subprocess.run(["lsblk", "-dn", "-o", "NAME,SERIAL"],
                            capture_output=True,check=True,text=True)
            for line in result.stdout.strip().split("\n"):
                parts = line.split(maxsplit=1)
                if len(parts) >=1 and parts[0] in self.disks:
                    serials[parts[0]] = parts[1] if len(parts) > 1 else "N/A"

                return serials if serials else []
                     
        except Exception as e:
            _log_error("Disk Serial No Failed",e)
            return["Error Fetching Disk Serial Number"]
        
        
        
    
           
if __name__ == "__main__":
   cds = Disk()
   print(cds.size())
#    print(cds.size())
    