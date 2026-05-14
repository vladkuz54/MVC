import csv
from datetime import datetime


class CSVReader:
    def __init__(self, filename):
        self.filename = filename

    def read_csv(self):
        data = []
        with open(self.filename, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, value in row.items():
                    if "timestamp" in key or "created_at" in key:
                        row[key] = datetime.fromisoformat(value)
                    elif key in ["device_status", "alert_is_resolved"]:
                        row[key] = True if value.lower() == "true" else False
                    elif key in ["reading_value"]:
                        row[key] = float(value)
                    elif value.isdigit():
                        row[key] = int(value)
                data.append(row)
        return data
