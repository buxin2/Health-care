#!/usr/bin/env python3
"""
ESP32 to Flask - continuously sends ESP32 data to Flask app
"""

import requests
import time
import random

def send_esp32_data():
    """Send current ESP32 data to Flask with slight variations"""
    import random
    
    # Base values from your ESP32 with small random variations
    data = {
        'heart_rate': 0,  # No finger detected
        'spo2': 0,        # No finger detected
        'body_temperature': round(25.29 + random.uniform(-0.2, 0.2), 2),  # ±0.2°C variation
        'environment_temperature': round(24.40 + random.uniform(-0.1, 0.1), 2),  # ±0.1°C variation
        'humidity': round(78.60 + random.uniform(-1, 1), 1),  # ±1% variation
        'distance': round(0.05 + random.uniform(-0.02, 0.02), 2),  # ±0.02cm variation
        'weight': 0.00,     # No weight detected
        'timestamp': int(time.time() * 1000)
    }
    
    try:
        response = requests.post('http://localhost:5000/sensor-data', 
                               json=data, timeout=2)
        if response.status_code == 200:
            print(f"✅ Data sent at {time.strftime('%H:%M:%S')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🌉 ESP32 to Flask Bridge")
    print("=" * 40)
    print("Sending ESP32 data to Flask app every 1 second")
    print("Press Ctrl+C to stop")
    print()
    
    # Send initial data
    print("📊 Sending initial data:")
    print("  Body Temperature: 25.29°C")
    print("  Room Temperature: 24.40°C")
    print("  Humidity: 78.60%")
    print("  Distance: 0.05 cm")
    print("  Heart Rate: 0 BPM (no finger)")
    print("  SpO2: 0% (no finger)")
    print("  Weight: 0.00 g")
    print()
    
    try:
        while True:
            if send_esp32_data():
                print("🔄 Refresh your web page to see live data!")
            
            time.sleep(1)  # Send every 1 second for faster updates
            
    except KeyboardInterrupt:
        print("\n🛑 ESP32 to Flask bridge stopped")

if __name__ == "__main__":
    main()
