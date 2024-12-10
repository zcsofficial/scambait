from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "logs.txt"

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/log', methods=['POST'])
def log():
    # Get device info from frontend
    data = request.json
    device_info = data.get('device_info', {})

    # Get user IP address
    user_ip = request.remote_addr

    # Fetch geolocation details
    geolocation = requests.get(f"http://ip-api.com/json/{user_ip}").json()

    # Log details
    logged_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IP": user_ip,
        "Device_Info": device_info,
        "Geolocation": geolocation,
    }

    # Save to file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(logged_data, indent=4) + "\n")

    print("Data logged:", logged_data)  # For debugging
    return jsonify({"status": "success", "data": logged_data})

if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0', port=5000)
