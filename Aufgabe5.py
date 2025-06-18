import psutil
import time
from datetime import datetime
from pymongo import MongoClient
import os

class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu is None or ram_total is None or ram_used is None or timestamp is None:
            self.cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            self.ram_total = mem.total
            self.ram_used = mem.used
            self.timestamp = datetime.now()
        else:
            self.cpu = cpu
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp

    def to_dict(self):
        return {
            "cpu": self.cpu,
            "ram_total": self.ram_total,
            "ram_used": self.ram_used,
            "timestamp": self.timestamp
        }

def main():
    uri = os.getenv("MONGO_URI")
    if not uri:
        print("MONGO_URI nicht gesetzt.")
        return

    client = MongoClient(uri)
    col = client["powerlogger"]["stats"]

    print("Logger läuft...")

    try:
        while True:
            p = Power()
            col.insert_one(p.to_dict())
            count = col.count_documents({})
            if count > 10000:
                diff = count - 10000
                col.delete_many({}, sort=[("timestamp", 1)], limit=diff)
            print(f"[{p.timestamp}] CPU: {p.cpu}% RAM: {p.ram_used // 1e6:.0f}/{p.ram_total // 1e6:.0f} MB")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Beendet.")

if __name__ == "__main__":
    main()
