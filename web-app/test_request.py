import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

url = os.getenv("INFLUX_URL") + "/api/v2/query"

headers = {
    "Authorization": f"Token {os.getenv('INFLUX_TOKEN')}",
    "Content-Type": "application/vnd.flux",
    "Accept": "application/csv"
}

query = '''
from(bucket: "motosense")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "vibration")
  |> filter(fn: (r) => r["_field"] == "rms")
  |> last()
'''

try:
    response = requests.post(
        url,
        params={"org": os.getenv("INFLUX_ORG")},
        headers=headers,
        data=query,
        timeout=20
    )

    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)

except Exception as e:
    print("ERROR:")
    print(e)