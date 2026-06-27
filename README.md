# MOTOSENSE: Vibration Monitoring System

MOTOSENSE is an industrial grade vibration monitoring system designed to track the health of mechanical components, specifically for the CVT system of the Honda Vario 160 motorcycle. This system utilizes a Raspberry Pi and ADXL345 sensor for real time data acquisition, edge processing for instant alerts, and cloud database integration for long term trend analysis.

## Project Overview
The system features two primary operational modes:
1. **Edge Processing (Offline):** The Raspberry Pi processes vibration data locally. If vibration exceeds thresholds, the system provides instant feedback via LED and buzzer indicators without requiring an internet connection.
2. **Remote Monitoring (Online):** When connected to the internet, the system synchronizes data to a cloud database (InfluxDB) for remote web dashboard visualization.

## Component List

| Component | Specification | Quantity |
| :--- | :--- | :--- |
| Raspberry Pi 3B | Computing Core | 1 Unit |
| MicroSD Card | 128GB (Minimum 32GB) | 1 Unit |
| GY-291 ADXL345 Module | I2C Vibration Sensor | 1 Unit |
| HW-479 RGB LED Module | Common Cathode | 1 Unit |
| Active Buzzer | Warning Alarm | 1 Unit |
| Power Bank | Minimum Output 5V/3A | 1 Unit |
| 40-pin GPIO Ribbon Cable | IDC Connector | 1 Unit |
| Protoboard | Circuit Board | 1 Unit |
| Solder & Solder Tin | Electrical Fixation Tool | 1 Set |
| Stranded Wire (AWG 22/24) | Copper Wire | As needed |
| Hard Box Casing | ABS/PETG Material | 1 Unit |
| Spacer/Standoff Bolt | M2.5 Size | As needed |
| Standard Bolt & Nut | M3 Size | As needed |
| Heatsink & Mini Fan | Cooling System | 1 Set |
| Cable Ties | Frame Fixator | As needed |
| Heat Shrink Tubing | Cable Insulator | As needed |

## Electrical Specifications

### Sensor (ADXL345)
* **VCC:** 3.3V (Pin 1)
* **GND:** Ground (Pin 9)
* **SDA:** GPIO 2 (Pin 3)
* **SCL:** GPIO 3 (Pin 5)

### Visual Indicator (RGB LED)
* **Red:** GPIO 17 (Pin 11) - Danger indicator.
* **Green:** GPIO 27 (Pin 13) - Normal operational indicator.
* **Blue:** GPIO 22 (Pin 15) - Warning/transition indicator.
* **Ground:** Ground (Pin 14)

### Actuators (Buzzer & Fan)
* **Buzzer VCC:** 5V (Pin 2)
* **Buzzer I/O:** GPIO 23 (Pin 16)
* **Fan Red:** 5V (Pin 4)
* **Fan Black:** Ground (Pin 20)

## Installation and Usage

1. **Edge Processing (Local):** The system runs as a background service (`motosense.service`). You can check the status with `sudo systemctl status motosense.service`.
2. **Calibration:** If readings are inaccurate, adjust the offset values in `calibration.json`.
3. **Physical Installation:** Attach the casing to the CVT using cable ties. Ensure the ADXL345 sensor is rigidly mounted to the casing base for accurate data capture.

## Project Information
* **Dashboard Access:** [https://kiiin.pythonanywhere.com/](https://kiiin.pythonanywhere.com/)