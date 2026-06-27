import os
import csv
from io import StringIO

import requests
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)

INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/latest")
def latest():

    url = f"{INFLUX_URL}/api/v2/query"

    headers = {
        "Authorization": f"Token {INFLUX_TOKEN}",
        "Content-Type": "application/vnd.flux",
        "Accept": "application/csv"
    }

    query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "vibration")
  |> filter(fn: (r) => r["_field"] == "rms")
  |> last()
'''

    try:

        response = requests.post(
            url,
            params={"org": INFLUX_ORG},
            headers=headers,
            data=query,
            timeout=20
        )

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": response.text
            }), 500

        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)

        rows = list(reader)

        if not rows:
            return jsonify({
                "status": "success",
                "rms": None,
                "time": None
            })

        row = rows[0]

        return jsonify({
            "status": "success",
            "time": row["_time"],
            "rms": float(row["_value"])
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)