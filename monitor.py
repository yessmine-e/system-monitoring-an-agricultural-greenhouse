# -*- coding: utf-8 -*-
import time
import json
import numpy as np
import pickle
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import dht11
import pandas as pd

# ------------------------------
# Configuration GPIO
# ------------------------------
DHT_PIN = 4        # GPIO du DHT11
BUZZER_PIN = 17    # GPIO du buzzer
PIR_PIN = 27       # GPIO du capteur de mouvement

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# ------------------------------
# MQTT / ThingsBoard
# ------------------------------
BROKER = "demo.thingsboard.io"
PORT = 1883
ACCESS_TOKEN = " "

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

# Callbacks pour debug
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion MQTT réussie !")
    else:
        print("Erreur de connexion MQTT, rc=", rc)

def on_publish(client, userdata, mid):
    print("Message publié avec id:", mid)

client.on_connect = on_connect
client.on_publish = on_publish

# Connexion et démarrage du loop
client.connect(BROKER, PORT, 60)
client.loop_start()

# ------------------------------
# Charger le modèle prédictif Temp+Hum
# ------------------------------
with open("model_temp_hum.pkl", "rb") as f:
    model = pickle.load(f)

# ------------------------------
# Initialisation des valeurs pour prédiction
# ------------------------------
df = pd.read_csv("data_decembre_tunisie.csv", encoding="ISO-8859-1")
df.columns = ["Timestamp", "Humidity", "Temperature_F", "Temperature_C"]

n_steps = 3
temp_values = df["Temperature_C"].iloc[-n_steps:].tolist()
hum_values  = df["Humidity"].iloc[-n_steps:].tolist()
last_gas = 0

# ------------------------------
# Initialisation DHT11
# ------------------------------
dht_instance = dht11.DHT11(pin=DHT_PIN)

# ------------------------------
# Fonction simulation gaz réaliste
# ------------------------------
def simulate_gas(temp, hum, last_gas):
    base = 0.5*temp + 0.3*hum
    event = np.random.choice([0, np.random.uniform(5, 20)], p=[0.9, 0.1])
    gas_value = 0.7*last_gas + 0.3*(base + event)
    return round(gas_value, 2)

# ------------------------------
# Boucle principale
# ------------------------------
try:
    while True:
        # Lecture DHT11
        result = dht_instance.read()
        if result.is_valid():
            temp_sensor = result.temperature
            hum_sensor = result.humidity
        else:
            temp_sensor = temp_values[-1]
            hum_sensor = hum_values[-1]

        # Prédiction Temp+Hum
        X_new = np.array([temp_values[-n_steps:] + hum_values[-n_steps:]]).reshape(1, -1)
        pred = model.predict(X_new)
        temp_pred = round(pred[0][0], 2)
        hum_pred  = round(pred[0][1], 2)

        # Simulation valeur gaz
        gas_value = simulate_gas(temp_pred, hum_pred, last_gas)
        last_gas = gas_value

        # Détection mouvement
        motion_detected = GPIO.input(PIR_PIN)

        # Contrôle buzzer uniquement sur mouvement
        if motion_detected:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        # Publication MQTT
        payload = json.dumps({
            "Temperature_Real": temp_sensor,
            "Humidity_Real": hum_sensor,
            "Temperature_Pred": temp_pred,
            "Humidity_Pred": hum_pred,
            "Gas": gas_value,
            "Motion": int(motion_detected)
        })
        result = client.publish("v1/devices/me/telemetry", payload)
        if result.rc != 0:
            print("Erreur publication MQTT, rc=", result.rc)
        print("Payload envoyé:", payload)

        # Mise à jour liste pour prochaine prédiction
        temp_values.append(temp_pred)
        hum_values.append(hum_pred)

        time.sleep(2)

except KeyboardInterrupt:
    print("Arrêt du script...")
finally:
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()


