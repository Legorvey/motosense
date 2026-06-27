import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient

# ==========================
# Load .env
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ==========================
# Ambil konfigurasi
# ==========================
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

print("=== Konfigurasi ===")
print("URL    :", INFLUX_URL)
print("ORG    :", INFLUX_ORG)
print("BUCKET :", INFLUX_BUCKET)
print("===================")

# ==========================
# Koneksi ke InfluxDB
# ==========================
try:
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    print("✓ Berhasil membuat client")

except Exception as e:
    print("✗ Gagal membuat client")
    print(e)
    exit()

# ==========================
# Query data terbaru
# ==========================
query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "vibration")
  |> filter(fn: (r) => r["_field"] == "rms")
  |> last()
'''

try:
    tables = client.query_api().query(query)

    found = False

    for table in tables:
        for record in table.records:
            found = True
            print("\n=== DATA TERBARU ===")
            print("Time :", record.get_time())
            print("Field:", record.get_field())
            print("Value:", record.get_value())

    if not found:
        print("\nTidak ada data ditemukan.")
        print("Pastikan Raspberry Pi sedang mengirim data dan subscriber berhasil menulis ke InfluxDB.")

except Exception as e:
    print("\nGagal menjalankan query:")
    print(e)