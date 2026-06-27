# MOTOSENSE: Vibration Monitoring System

This project is an industrial-grade vibration monitoring system designed to track the health of mechanical components—specifically for a motorcycle's CVT system—by measuring RMS (Root Mean Square) vibration levels. It provides real-time data collection via hardware sensors and a live web-based dashboard for analysis.

## Project Overview
The system consists of two main parts:
1.  **Hardware (Data Collection):** A Raspberry Pi connected to an accelerometer sensor (ADXL345) that captures vibration data and sends it to a cloud database.
2.  **Dashboard (Visualization):** A web interface that pulls data from the cloud and displays it on an interactive chart, allowing users to monitor vibration trends and identify when maintenance might be required.

## How It Works
*   **Data Flow:** The Raspberry Pi continuously reads vibration data from the sensor. This data is transmitted to an InfluxDB cloud database.
*   **Visualization:** The web dashboard connects to the cloud database, retrieves the latest vibration values, and plots them on a graph.

## System Setup

### Hardware Requirements
*   Raspberry Pi (with internet connectivity)
*   ADXL345 Accelerometer sensor
*   MQTT Broker (for data transmission)

### Software Requirements
*   Python 3.x
*   InfluxDB (for data storage)
*   Web Browser (to view the dashboard)

## Installation & Usage

### 1. Data Collection (Raspberry Pi)
*   Ensure all necessary Python libraries are installed within your environment.
*   Run the main collection script: 
    `/home/rayram34/motosense_env/bin/python /home/rayram34/motosense_main.py`
*   Ensure the MQTT broker is active to allow data to move from the hardware to the database.

### 2. Web Dashboard
*   The dashboard is built using HTML, CSS, and JavaScript with the Chart.js library for data visualization.
*   The dashboard retrieves data directly from the InfluxDB cloud using a secure token.
*   **Access:** You can view the live dashboard here: [https://kiiin.pythonanywhere.com/](https://kiiin.pythonanywhere.com/)

## Maintenance
*   **Service Monitoring:** On the Raspberry Pi, vibration data collection is managed as a background service. You can check the status using `sudo systemctl status motosense.service`.
*   **Calibration:** If the sensor readings appear inaccurate, refer to `calibration.json` to update the baseline offsets for the X, Y, and Z axes.