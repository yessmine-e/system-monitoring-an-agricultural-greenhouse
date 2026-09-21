# 🌱 IoT Greenhouse Monitoring System

## Introduction

This project implements an edge-to-cloud IoT system for affordable, intelligent greenhouse monitoring. It integrates DHT22, PIR, and MQ-2 sensors on a Raspberry Pi with real-time MQTT publishing to ThingsBoard, combining real-time monitoring, automated alerting, and on-device (edge) AI prediction.

## ⚙️ How It Works

1. Environmental sensors (DHT22 for temperature/humidity, PIR for motion, MQ-2 for gas) collect real-time data on the Raspberry Pi.
2. Sensor readings are published in real time via MQTT (paho-mqtt) to a ThingsBoard cloud dashboard.
3. ThingsBoard Rule Chains automatically trigger critical alarms when gas levels exceed a defined threshold.
4. A GPIO-controlled buzzer is activated locally on motion detection, providing immediate on-site alerting.
5. An interactive real-time dashboard on ThingsBoard displays live sensor data and alarm history.
6. A Random Forest regression model, trained on locally collected data, runs directly on the Raspberry Pi to forecast future temperature and humidity trends.

## 🧠 Edge AI Component

Rather than relying solely on cloud-based processing, this project brings prediction directly to the edge:

- **On-device inference**: the Random Forest regression model is trained and deployed locally on the Raspberry Pi, enabling temperature and humidity forecasting without depending on a constant cloud connection.
- **Self-collected dataset**: the training data was gathered locally in Tunisia under real greenhouse conditions, rather than using a generic public dataset, making the model more representative of the actual deployment environment.
- **Low-resource design**: Random Forest was chosen for its balance between predictive accuracy and computational efficiency, making it suitable for continuous execution on Raspberry Pi-class hardware.

## 🔑 Key Features

- Real-time environmental monitoring (temperature, humidity, motion, gas)
- Automated critical alarms via ThingsBoard Rule Chains on gas threshold breaches
- Local, low-latency alerting through a GPIO-driven buzzer on motion detection
- Interactive real-time dashboard for remote monitoring
- Edge AI forecasting of temperature and humidity using Random Forest

## 🛠️ Tech Stack

- **Hardware**: Raspberry Pi, DHT22, PIR (HC-SR501), MQ-2, GPIO
- **Communication**: MQTT (paho-mqtt)
- **Cloud platform**: ThingsBoard (Rule Chains, real-time dashboard)
- **Machine Learning**: Python, scikit-learn (Random Forest Regression)

## 🚀 Installation & Usage

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Run the monitoring script:
```bash
python monitor.py
```

Train the Random Forest model (if retraining is needed):
```bash
python train_random_forest.py
```

> Note: MQTT broker credentials and ThingsBoard device tokens should be configured via environment variables or a `.env` file, not hardcoded in the source code.
