import csv
import random
from datetime import datetime, timedelta


class CSVGenerator:
    def __init__(self, filename="readings.csv", num_rows=100):
        self.filename = filename
        self.num_rows = num_rows

    def random_organization(self):
        name = ["Acme Corp", "Globex Inc", "Initech", "Umbrella Corp", "Hooli"]
        api_key = ["abc123", "def456", "ghi789", "jkl012", "mno345"]
        created_at = datetime.now() - timedelta(days=random.randint(1, 365))
        return {
            "name": random.choice(name),
            "api_key": random.choice(api_key),
            "created_at": created_at.strftime("%Y-%m-%d"),
        }

    def random_device(self):
        devices = [
            {
                "mac_address": "02:00:00:00:00:01",
                "status": True,
                "firmware_version": "1.0.0",
            },
            {
                "mac_address": "02:00:00:00:00:02",
                "status": False,
                "firmware_version": "1.1.0",
            },
            {
                "mac_address": "02:00:00:00:00:03",
                "status": True,
                "firmware_version": "1.2.0",
            },
            {
                "mac_address": "02:00:00:00:00:04",
                "status": False,
                "firmware_version": "1.3.0",
            },
            {
                "mac_address": "02:00:00:00:00:05",
                "status": True,
                "firmware_version": "1.4.0",
            },
            {
                "mac_address": "02:00:00:00:00:06",
                "status": False,
                "firmware_version": "1.5.0",
            },
            {
                "mac_address": "02:00:00:00:00:07",
                "status": True,
                "firmware_version": "1.6.0",
            },
            {
                "mac_address": "02:00:00:00:00:08",
                "status": False,
                "firmware_version": "1.7.0",
            },
            {
                "mac_address": "02:00:00:00:00:09",
                "status": True,
                "firmware_version": "1.8.0",
            },
            {
                "mac_address": "02:00:00:00:00:0a",
                "status": False,
                "firmware_version": "1.9.0",
            },
            {
                "mac_address": "02:00:00:00:00:0b",
                "status": True,
                "firmware_version": "2.0.0",
            },
            {
                "mac_address": "02:00:00:00:00:0c",
                "status": False,
                "firmware_version": "2.1.0",
            },
            {
                "mac_address": "02:00:00:00:00:0d",
                "status": True,
                "firmware_version": "2.2.0",
            },
            {
                "mac_address": "02:00:00:00:00:0e",
                "status": False,
                "firmware_version": "2.3.0",
            },
            {
                "mac_address": "02:00:00:00:00:0f",
                "status": True,
                "firmware_version": "2.4.0",
            },
            {
                "mac_address": "02:00:00:00:00:10",
                "status": False,
                "firmware_version": "2.5.0",
            },
            {
                "mac_address": "02:00:00:00:00:11",
                "status": True,
                "firmware_version": "2.6.0",
            },
            {
                "mac_address": "02:00:00:00:00:12",
                "status": False,
                "firmware_version": "2.7.0",
            },
            {
                "mac_address": "02:00:00:00:00:13",
                "status": True,
                "firmware_version": "2.8.0",
            },
            {
                "mac_address": "02:00:00:00:00:14",
                "status": False,
                "firmware_version": "2.9.0",
            },
        ]

        return {
            "mac_address": random.choice([device["mac_address"] for device in devices]),
            "status": random.choice([device["status"] for device in devices]),
            "firmware_version": random.choice(
                [device["firmware_version"] for device in devices]
            ),
        }

    def random_sensor(self):
        sensor_types = ["temperature", "humidity", "pressure", "light", "motion"]
        units = {
            "temperature": "°C",
            "humidity": "%",
            "pressure": "hPa",
            "light": "lux",
            "motion": "motion detected",
        }
        sensor_type = random.choice(sensor_types)
        return {
            "type": sensor_type,
            "unit": units[sensor_type],
        }

    def random_reading(self):
        value = round(random.uniform(0, 100), 2)
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 1000))
        return {
            "value": value,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def random_alert(self):
        severity = random.choice(["low", "medium", "high"])
        message = random.choice(
            [
                "Temperature threshold exceeded",
                "Humidity level too low",
                "Pressure drop detected",
                "Light level too high",
                "Motion detected in restricted area",
            ]
        )
        is_resolved = random.choice([True, False])
        return {
            "severity": severity,
            "message": message,
            "is_resolved": is_resolved,
        }

    def generate_csv(self):
        filepath = f"{self.filename}"

        with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "organization_name",
                    "organization_api_key",
                    "organization_created_at",
                    "device_mac_address",
                    "device_status",
                    "device_firmware_version",
                    "sensor_type",
                    "sensor_unit",
                    "reading_value",
                    "reading_timestamp",
                    "alert_severity",
                    "alert_message",
                    "alert_is_resolved",
                ]
            )

            for _ in range(self.num_rows):
                organization = self.random_organization()
                device = self.random_device()
                sensor = self.random_sensor()
                reading = self.random_reading()
                alert = self.random_alert()

                writer.writerow(
                    [
                        organization["name"],
                        organization["api_key"],
                        organization["created_at"],
                        device["mac_address"],
                        device["status"],
                        device["firmware_version"],
                        sensor["type"],
                        sensor["unit"],
                        reading["value"],
                        reading["timestamp"],
                        alert["severity"],
                        alert["message"],
                        alert["is_resolved"],
                    ]
                )
        print(f"CSV file '{self.filename}' generated with {self.num_rows} rows.")


generator = CSVGenerator(filename="readings.csv", num_rows=100)


if __name__ == "__main__":
    generator.generate_csv()
