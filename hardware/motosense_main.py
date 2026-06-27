import smbus2 as smbus
import time
import math
import json
import ssl
import os
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# --- MUAT ENVIRONMENT VARIABLES ---
# Pastikan file .env berada di direktori yang sama dengan script ini
load_dotenv()

# --- CONFIGURATION ---
ADXL_ADDRESS = 0x53

# Konfigurasi MQTT
MQTT_BROKER = "ea9fb4561d1848b7aa69cee6b67dcb67.s1.eu.hivemq.cloud"
MQTT_PORT = 8883                 
MQTT_USERNAME = "kiiin"          
MQTT_PASSWORD = "Kin067509"      
MQTT_TOPIC = "motosense/rms"

# Konfigurasi InfluxDB (Diambil dari .env)
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

# --- LOAD CALIBRATION ---
try:
    with open('calibration.json', 'r') as f:
        cal_data = json.load(f)
        x_offset = cal_data['x_offset']
        y_offset = cal_data['y_offset']
        z_offset = cal_data['z_offset']
        print(f"Loaded Calibration: X={x_offset:.3f}, Y={y_offset:.3f}, Z={z_offset:.3f}")
except FileNotFoundError:
    print("CRITICAL ERROR: 'calibration.json' not found.")
    print("You must run 'python3 calibrate.py' first.")
    exit()

# --- GPIO SETUP ---
LED_R, LED_G, BUZZER = 17, 27, 23
GPIO.setmode(GPIO.BCM)
GPIO.setup([LED_R, LED_G, BUZZER], GPIO.OUT)

# LED dimulai dari LOW (Mati), Buzzer dimulai dari HIGH (Mati)
GPIO.output([LED_R, LED_G], GPIO.LOW)
GPIO.output(BUZZER, GPIO.HIGH)

# --- I2C SETUP ---
bus = smbus.SMBus(1)
bus.write_byte_data(ADXL_ADDRESS, 0x2D, 0x08)
bus.write_byte_data(ADXL_ADDRESS, 0x31, 0x0A)

# --- MQTT SETUP ---
print("Menghubungkan ke HiveMQ...")
client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
print("✅ Terhubung ke MQTT!")

# --- INFLUXDB SETUP ---
print("Menyiapkan koneksi InfluxDB...")
client_db = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_db.write_api(write_options=SYNCHRONOUS)
print("✅ InfluxDB siap!")

# --- FUNGSI BACA SENSOR ---
def get_acceleration():
    data = bus.read_i2c_block_data(ADXL_ADDRESS, 0x32, 6)
    x = data[0] | (data[1] << 8)
    y = data[2] | (data[3] << 8)
    z = data[4] | (data[5] << 8)
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536
    
    gx = (x * 0.004) + x_offset
    gy = (y * 0.004) + y_offset
    gz = (z * 0.004) + z_offset
    return gx, gy, gz

# --- MAIN LOOP ---
try:
    print("\nMOTOSENSE Active. Membaca getaran...\n")
    while True:
        samples = []
        for _ in range(50):
            gx, gy, gz = get_acceleration()
            mag = math.sqrt(gx**2 + gy**2 + gz**2)
            samples.append(mag)
            time.sleep(0.01)
            
        # Kalkulasi RMS
        rms_g = math.sqrt(sum([s**2 for s in samples]) / len(samples))
        rms_velocity_mms = rms_g * 9.81 * 1000 
        
        # 1. Publish ke MQTT (Untuk Web Dashboard Real-time)
        client.publish(MQTT_TOPIC, f"{rms_velocity_mms:.2f}")
        
        # 2. Tulis ke InfluxDB (Untuk Riwayat Database)
        try:
            point = Point("vibration").field("rms", float(rms_velocity_mms))
            write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
            print(f"RMS Velocity: {rms_velocity_mms:.2f} mm/s | RMS G: {rms_g:.2f} | 📡 Data terkirim (MQTT & DB)")
        except Exception as e:
            print(f"RMS Velocity: {rms_velocity_mms:.2f} mm/s | ❌ Gagal simpan ke InfluxDB: {e}")
        
        # 3. Logika Indikator Fisik
        if rms_g > 1.5:
            GPIO.output(LED_R, GPIO.HIGH)
            GPIO.output(LED_G, GPIO.LOW)
            GPIO.output(BUZZER, GPIO.LOW)  # LOW = Buzzer Menyala (Active-LOW)
        else:
            GPIO.output(LED_R, GPIO.LOW)
            GPIO.output(LED_G, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.HIGH) # HIGH = Buzzer Mati (Active-LOW)
            
except KeyboardInterrupt:
    print("\nMenutup sistem dengan aman...")
    GPIO.cleanup()
    client.loop_stop()
    client_db.close() # Menutup koneksi database
    print("System Offline.")