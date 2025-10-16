# 🛰️ Telem — Sensor Telemetry Backend & CLI

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-green)](https://flask.palletsprojects.com/)
[![Click](https://img.shields.io/badge/CLI-Click-orange)](https://click.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Status-WIP-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)]()

> **Telem** is a telemetry system that connects hardware sensors to a Flask backend using a Python CLI.  
> The goal: enable users to **stream live sensor data** or upload batch readings seamlessly for analysis and alerting.

---

## 🌟 Highlights

Telem allows users to:

1. **Register and authenticate** via CLI  
2. **Register sensors** with metadata (location, type, description)  
3. **Stream live data** from an serial sensors (e.g., HC-SR04 distance sensor)  
4. **Batch upload readings** to the backend for storage and later analysis  

The backend provides CRUD routes for sensors and their data, while the CLI offers a simple interface to push or fetch telemetry readings.

---

## 💡 Overview
**NOTE**: The project is still under development and is only functional locally. A dedicated backend will be launched soon, which will only require users to configure the CLI. 

Telem is a Python-based telemetry system that connects physical sensors, like those attached to an Arduino, to a Flask backend through a command-line interface (CLI). It allows users to register sensors, stream or batch-upload readings, and store them in a database for analysis. Designed with modularity in mind, Telem separates hardware communication, data processing, and API logic, making it easy to extend with new sensor types, data units, or alerting features. It’s a lightweight, end-to-end foundation for building scalable telemetry and IoT-style backend systems.

---

## ⚙️ Tech Stack

| Layer | Technology | Description |
|-------|-------------|-------------|
| **Backend** | Flask (Python) | REST API for authentication, sensor registration, and data ingestion |
| **Database** | SQLite → PostgreSQL | Currently uses SQLite (local), will migrate to Postgres for deployment |
| **ORM** | SQLAlchemy | Models and queries for users, sensors, and data |
| **Authentication** | Flask-JWT-Extended | Secure JWT-based authentication |
| **CLI** | Click | Command-line interface for user interaction |
| **Hardware Interface** | PySerial | Reads live data from Arduino/serial devices |
| **Data Format** | JSON over HTTP | CLI sends telemetry data in JSON batches |


### 🧑‍💻 Authors

[Cody Cole](https://www.codycode.org/)
Software Engineer & U.S. Army Veteran

---

## 🚀 Usage

Using CLI to login, register a sensor, and stream sensor data from an Arduino/HC-SR04 distance sensor setup. Port, baud, and batch size are configurable. 

```py
❯ telem login codycode2 Testpassword2!@#$
                       
{
    "status": "success",
    "token_saved": true
}

❯ telem register-sensor sentry-1 --latitude 34.0549 --longitude 118.2426 --description "Watch the fort"

{
    "created_at": "2025-10-16T18:34:31",
    "description": "Watch the fort",
    "id": 4,
    "is_active": true,
    "latitude": 34.0549,
    "longitude": 118.2426,
    "type": "sentry-1",
    "user_id": 1
}

❯ telem stream-serial --sensor-id 4 --unit "centimeters" --batch-size 10

Attempting to read live data from /dev/cu.usbmodem1101 (baud 9600)
Port is open!
Reading gathered: {'unit': 'cm', 'value': 8.99}
Reading gathered: {'unit': 'cm', 'value': 9.31}
Reading gathered: {'unit': 'cm', 'value': 8.99}
Reading gathered: {'unit': 'cm', 'value': 9.31}
Reading gathered: {'unit': 'cm', 'value': 11.4}
Reading gathered: {'unit': 'cm', 'value': 11.99}
Reading gathered: {'unit': 'cm', 'value': 12.54}
Reading gathered: {'unit': 'cm', 'value': 11.87}
Reading gathered: {'unit': 'cm', 'value': 12.76}
Reading gathered: {'unit': 'cm', 'value': 20.72}
Batch size reached
[
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 76,
        "sensor_id": 4,
        "unit": "cm",
        "value": 8.99
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 77,
        "sensor_id": 4,
        "unit": "cm",
        "value": 9.31
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 78,
        "sensor_id": 4,
        "unit": "cm",
        "value": 8.99
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 79,
        "sensor_id": 4,
        "unit": "cm",
        "value": 9.31
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 80,
        "sensor_id": 4,
        "unit": "cm",
        "value": 11.4
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 81,
        "sensor_id": 4,
        "unit": "cm",
        "value": 11.99
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 82,
        "sensor_id": 4,
        "unit": "cm",
        "value": 12.54
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 83,
        "sensor_id": 4,
        "unit": "cm",
        "value": 11.87
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 84,
        "sensor_id": 4,
        "unit": "cm",
        "value": 12.76
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 85,
        "sensor_id": 4,
        "unit": "cm",
        "value": 20.72
    }
]

❯ telem get-sensor-data 4                                               

[
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 76,
        "sensor_id": 4,
        "unit": "cm",
        "value": 8.99
    },
    {
        "created_at": "2025-10-16T18:36:46",
        "id": 77,
        "sensor_id": 4,
        "unit": "cm",
        "value": 9.31
    },
    ...
]

❯ telem get-sensors      

[
    {
        "created_at": "2025-10-16T18:34:31",
        "description": "Watch the fort",
        "id": 4,
        "is_active": true,
        "latitude": 34.0549,
        "longitude": 118.2426,
        "type": "sentry-1",
        "user_id": 1
    }
]
```

---

## ⬇️ Installation
As stated, the backend is currently only setup for local usage. For future usage, the user will only have to install the CLI with pip. Until then, both packages (backend and CLI) need to be cloned and built. Get the backend up and running on terminal 1 and use the CLI in terminal 2. 

```bash
TERMINAL 1 - BACKEND
git clone https://github.com/colecody27/telem-api
cd telem-api

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 run.py


TERMINAL 2 - CLI
git clone https://github.com/colecody27/telem-cli
cd telem-cli

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip3 install -e .

telem
```

---

## 🧠 Planned Features (TODO)
🧮 CLI Enhancements

 - Add ability to read from file (CSV or JSON)
 - Improve serial data parsing and flexible input options
 - Package and publish CLI to PyPI
 - Add commands to hit all backend routes

📊 Data & Analytics

 - Query sensor data by time range
 - Add data conversions, scaling, and offsets
 - Implement aggregation routes (avg, min, max, over time)

🖥️ Device & Alerting

- Add Device model (each device will have multiple sensors)
- Define threshold-based alerts per device/sensor
- Enable real-time notification triggers and scanning

🗄️ Infrastructure

 - Migrate from SQLite to PostgreSQL
 - Deploy backend

---

## 🫡 Feedback and Contributing

Lots of improvements to be made! I welcome any feedback and contributions. 
[Issues](https://github.com/colecody27/iot-api/issues)

---

