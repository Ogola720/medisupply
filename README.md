# 🏥 Medical Supply Chain IoT Dashboard

![Project Banner](https://github.com/Ogola720/medisupply/blob/0193253d21ec531a9cc811023aa1782343cba99c/assets/images/Screenshot%20(4907).png)

> A real-time IoT dashboard that monitors, logs, and tracks the supply chain of medical equipment and drugs using **ESP32**, **MQTT (HiveMQ)**, **Firebase**, and **Python Dash**.

---

## 🚀 Project Overview

This project simulates a smart medical supply chain monitoring system. It leverages:

* 📡 **ESP32** microcontroller (simulated on Wokwi)
* 🔗 **MQTT Protocol** via **HiveMQ** for real-time data streaming
* 🖥️ **Python Dash** for interactive UI & analytics
* 🔥 **Firebase** for historical data storage and sync

Real-time events such as `arrival`, `dispatch`, temperature, and humidity readings are published by the ESP32 and consumed by a Dash-powered web dashboard. Retained messages ensure persistent state visibility across sessions.

---

## 🧱 Features

* ✅ MQTT Broker connection & topic subscriptions
* 📨 Real-time updates for:

  * Arrival and Dispatch events
  * Environment Monitoring (Temperature & Humidity)
  * Supply Chain Summary Data
* 📋 Logging panel for debugging and event tracing
* 🔄 Retained MQTT message handling
* 🔥 Firebase integration for optional cloud storage
* 📊 Graphs and Counters for trends and summaries

---

## ⚙️ Tech Stack

| Technology    | Purpose                          |
| ------------- | -------------------------------- |
| ESP32 (Wokwi) | IoT device simulator             |
| HiveMQ        | MQTT broker                      |
| MQTT.js       | JavaScript MQTT client (UI test) |
| Dash (Python) | Data dashboard                   |
| Firebase      | Optional cloud data sync         |
| Plotly        | Visualization engine             |

---

## 🔧 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/medical-iot-dashboard.git
cd medical-iot-dashboard
```

2. **Set Up Python Environment**

```bash
pip install -r requirements.txt
```

3. **Run the Dashboard**

```bash
python app.py
```

4. **Simulate Data on Wokwi (ESP32)**

* [Wokwi Simulation Link](#) (https://wokwi.com/projects/435671860997625857)

---

## 📸 Screenshots

### 🔹 Dashboard UI

| Live Dashboard View                               | MQTT Log Panel                                | Analytics Panel                                      |
| ------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------- |
| ![](./assets/images/screenshots/dashboard-ui.png) | ![](./assets/images/screenshots/mqtt-log.png) | ![](./assets/images/screenshots/analytics-panel.png) |

### 🔹 Firebase Console

> Showcase of Firebase Realtime Database or Firestore entries:

![Firebase Screenshot](./assets/images/screenshots/firebase-console.png)

### 🔹 Wokwi Platform

> Showcase of Wokwi simulation environment:

![Wokwi Screenshot](https://github.com/Ogola720/medisupply/blob/ded26c3217b24d8bec6d600f98646b7e480a8458/assets/images/Screenshot%20(4925)%20-%20Copy.png)

<details>
<summary>✨ Click to animate preview</summary>

![Animated View](./assets/images/screenshots/dashboard-animated.gif)

</details>

---

## 🔐 Firebase Setup (Optional)

1. Create a Firebase project
2. Add a Realtime Database
3. Copy your Firebase credentials into a file named `firebase_config.json`
4. Make sure this file is in your root directory and not tracked in version control
5. Enable database rules as needed to allow read/write access during testing

---

## 📂 Folder Structure

```
📦 medical-iot-dashboard
├── app.py
├── mqtt_client.py
├── firebase_service.py
├── assets/
│   └── images/
│       └── screenshots/
├── templates/
├── .env
└── README.md
```

---

## 💡 Future Improvements

* Add authentication layer for secured dashboard access
* Send alerts via SMS/email using Twilio or SendGrid
* Add device control (actuators) from the dashboard
* Use PostgreSQL for structured storage alongside Firebase

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Acknowledgements

* [HiveMQ Public Broker](https://www.hivemq.com/public-mqtt-broker/)
* [Wokwi Simulator](https://wokwi.com/)
* [Firebase](https://firebase.google.com/)
* [Dash by Plotly](https://dash.plotly.com/)

> *Built with ❤️ by \[Ogola Peter]*
