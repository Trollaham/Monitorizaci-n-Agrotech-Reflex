import paho.mqtt.client as mqtt
import requests
import logging
import time
import re
from datetime import datetime
from typing import Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("MAIoTA_MQTT")
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "Awi7LJfyyn6LPjg/15046220"
API_BASE_URL = "http://localhost:8000/api"
SENSOR_MAPPING = {
    "D1": {"id": "SENS-002", "factor": 0.01, "unit": "C", "type": "temperature"},
    "D2": {"id": "SENS-004", "factor": 0.01, "unit": "%", "type": "humidity"},
    "D3": {"id": "SENS-001", "factor": 0.01, "unit": "%", "type": "soil_moisture"},
    "D4": {"id": "SENS-003", "factor": 0.1, "unit": "lx", "type": "light"},
    "D5": {"id": "SENS-005", "factor": 0.1, "unit": "ppm", "type": "co2"},
    "D6": {"id": "SENS-006", "factor": 0.1, "unit": "ppb", "type": "voc"},
    "D7": {"id": "SENS-007", "factor": 0.1, "unit": "ppb", "type": "nox"},
}


class MAIoTAMQTTClient:
    def __init__(self):
        self.client = mqtt.Client(client_id="Reflex_Agrotech_Client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT Broker: {MQTT_BROKER}")
            client.subscribe(MQTT_TOPIC)
            logger.info(f"Subscribed to topic: {MQTT_TOPIC}")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logger.warning("Disconnected from MQTT Broker")
        if rc != 0:
            logger.warning("Unexpected disconnection. Attempting reconnect...")
            try:
                client.reconnect()
            except Exception as e:
                logger.exception(f"Reconnection failed: {e}")

    def parse_payload(self, payload_str: str) -> dict[str, float]:
        """
        Parses the payload string: CIoTA-D1=2603&D2=5411&...
        Returns a dict of {key: raw_value}
        """
        if not payload_str.startswith("CIoTA-"):
            logger.warning(f"Invalid payload format (missing prefix): {payload_str}")
            return {}
        clean_payload = payload_str.replace("CIoTA-", "")
        data = {}
        pairs = clean_payload.split("&")
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=")
                try:
                    data[key] = float(value)
                except ValueError:
                    logger.exception(f"Could not parse value for {key}: {value}")
        return data

    def process_data(self, data: dict[str, float]):
        """
        Process parsed data, apply factors, and send to API.
        """
        timestamp = datetime.utcnow().isoformat()
        for key, raw_value in data.items():
            if key in SENSOR_MAPPING:
                mapping = SENSOR_MAPPING[key]
                processed_value = raw_value * mapping["factor"]
                processed_value = round(processed_value, 2)
                payload = {
                    "value": processed_value,
                    "unit": mapping["unit"],
                    "timestamp": timestamp,
                    "type": mapping["type"],
                }
                self.send_to_api(mapping["id"], payload)

    def send_to_api(self, sensor_unique_id: str, payload: dict):
        url = f"{API_BASE_URL}/sensors/{sensor_unique_id}/data"
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                logger.info(
                    f"Data sent for {sensor_unique_id}: {payload['value']} {payload['unit']}"
                )
            elif response.status_code == 404:
                logger.warning(
                    f"Sensor {sensor_unique_id} not found in backend. Skipping."
                )
            else:
                logger.error(
                    f"Failed to send data for {sensor_unique_id}. Status: {response.status_code}, Response: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            logger.exception(f"API Request failed for {sensor_unique_id}: {e}")

    def on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode("utf-8")
            logger.info(f"Received payload: {payload_str}")
            parsed_data = self.parse_payload(payload_str)
            if parsed_data:
                self.process_data(parsed_data)
        except Exception as e:
            logger.exception(f"Error processing message: {e}")

    def run(self):
        logger.info("Starting MAIoTA MQTT Client...")
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            logger.exception("Stopping MQTT Client...")
            self.client.disconnect()
        except Exception as e:
            logger.exception(f"Fatal error in MQTT Client: {e}")


if __name__ == "__main__":
    client = MAIoTAMQTTClient()
    client.run()