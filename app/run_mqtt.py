from app.mqtt_client import MAIoTAMQTTClient

if __name__ == "__main__":
    print("Launching MQTT Client Service...")
    print("Press Ctrl+C to stop.")
    client = MAIoTAMQTTClient()
    client.run()