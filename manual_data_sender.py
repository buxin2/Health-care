#!/usr/bin/env python3
"""
Manual data sender - sends test data to Flask app
"""

import requests
import time
import json

def send_test_data():
    print("📡 Sending test sensor data to Flask app...")
    
    # Test data based on what you showed me
    test_data = {
        'heart_rate': 0,  # No finger detected
        'spo2': 0,        # No finger detected  
        'body_temperature': 25.29,  # From your ESP32 output
        'environment_temperature': 24.40,  # From your ESP32 output
        'humidity': 78.60,  # From your ESP32 output
        'distance': 50.0,   # Simulated distance
        'weight': 0.0,      # No weight detected
        'timestamp': int(time.time() * 1000)
    }
    
    print("📊 Test data:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    
    try:
        response = requests.post('http://localhost:5000/sensor-data', 
                               json=test_data, timeout=5)
        if response.status_code == 200:
            print("✅ Data sent to Flask successfully!")
            print("🔄 Refreshing web page to see the data...")
        else:
            print(f"❌ Flask error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending data: {e}")

def send_live_data():
    print("🔄 Sending live data every 5 seconds...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Simulate live data with some variation
            import random
            
            live_data = {
                'heart_rate': random.randint(0, 80),  # 0 when no finger
                'spo2': random.randint(0, 100),       # 0 when no finger
                'body_temperature': 25.29 + random.uniform(-0.5, 0.5),
                'environment_temperature': 24.40 + random.uniform(-0.3, 0.3),
                'humidity': 78.60 + random.uniform(-2, 2),
                'distance': random.uniform(30, 70),
                'weight': random.uniform(0, 10),
                'timestamp': int(time.time() * 1000)
            }
            
            print(f"📡 Sending data at {time.strftime('%H:%M:%S')}")
            
            try:
                response = requests.post('http://localhost:5000/sensor-data', 
                                       json=live_data, timeout=2)
                if response.status_code == 200:
                    print("✅ Data sent successfully!")
                else:
                    print(f"❌ Error: {response.status_code}")
            except Exception as e:
                print(f"❌ Send error: {e}")
            
            time.sleep(5)  # Send every 5 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Stopped sending data")

if __name__ == "__main__":
    print("🔧 Manual Data Sender")
    print("=" * 40)
    print("1. Send test data once")
    print("2. Send live data continuously")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "1":
        send_test_data()
    elif choice == "2":
        send_live_data()
    else:
        print("Invalid choice")
