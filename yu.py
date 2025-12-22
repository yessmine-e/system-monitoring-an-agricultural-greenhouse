import paho.mqtt.client as mqtt
import json
import time

BROKER = "demo.thingsboard.io"
PORT = 1883
ACCESS_TOKEN = "" 


client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

# Connexion
client.connect(BROKER, PORT, 60)
client.loop_start()  


def test_publish():
    for i in range(5):
        payload = json.dumps({"Temperature": 25 + i, "Humidity": 50 + i})
        result = client.publish("v1/devices/me/telemetry", payload)
        print(f"Message {i} publié:", payload, "Résultat:", result.rc)
        time.sleep(2)

if __name__ == "__main__":
    test_publish()
    client.loop_stop()
    client.disconnect()

