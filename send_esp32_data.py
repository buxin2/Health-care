#!/usr/bin/env python3
"""
Send ESP32 data to Flask app
"""

import requests
import time

def send_esp32_data():
    # Data from your ESP32 output
    data = {
        'heart_rate': 0,
        'spo2': 0,
        'body_temperature': 25.29,
        'environment_temperature': 24.40,
        'humidity': 78.60,
        'distance': 0.05,
        'weight': 0.00,
        'timestamp': int(time.time() * 1000)
    }
    
    print("📊 Sending ESP32 data to Flask:")
    for key, value in data.items():
        print(f"  {key}: {value}")
    
    try:
        response = requests.post('http://localhost:5000/sensor-data', 
                               json=data, timeout=5)
        if response.status_code == 200:
            print("✅ Data sent successfully!")
            print("🔄 Refresh your web page to see the data!")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_esp32_data()
