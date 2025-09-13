#!/usr/bin/env python3
"""
ESP32 Data Bridge - reads ESP32 data and sends to Flask
Run this while Arduino Serial Monitor is open
"""

import requests
import time
import re

def parse_esp32_data(text):
    """Parse ESP32 output text to extract sensor values"""
    data = {
        'heart_rate': 0,
        'spo2': 0,
        'body_temperature': 0,
        'environment_temperature': 0,
        'humidity': 0,
        'distance': 0,
        'weight': 0,
        'timestamp': int(time.time() * 1000)
    }
    
    try:
        # Extract room temperature
        room_temp_match = re.search(r'Room Temp: ([\d.]+)', text)
        if room_temp_match:
            data['environment_temperature'] = float(room_temp_match.group(1))
        
        # Extract humidity
        humidity_match = re.search(r'Humidity: ([\d.]+)', text)
        if humidity_match:
            data['humidity'] = float(humidity_match.group(1))
        
        # Extract body temperature
        body_temp_match = re.search(r'Temperature: ([\d.]+)', text)
        if body_temp_match:
            data['body_temperature'] = float(body_temp_match.group(1))
        
        # Set default values for other sensors
        data['distance'] = 50.0  # Default distance
        data['weight'] = 0.0     # No weight detected
        
    except Exception as e:
        print(f"Error parsing data: {e}")
    
    return data

def send_to_flask(data):
    """Send data to Flask app"""
    try:
        response = requests.post('http://localhost:5000/sensor-data', 
                               json=data, timeout=2)
        if response.status_code == 200:
            print("✅ Data sent to Flask successfully!")
            return True
        else:
            print(f"❌ Flask error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flask error: {e}")
        return False

def main():
    print("🌉 ESP32 Data Bridge")
    print("=" * 50)
    print("This script will send ESP32 data to Flask app")
    print("Make sure Arduino Serial Monitor is open and showing ESP32 data")
    print("Press Ctrl+C to stop")
    print()
    
    # Sample data based on your ESP32 output
    sample_data = {
        'heart_rate': 0,
        'spo2': 0,
        'body_temperature': 25.29,
        'environment_temperature': 24.40,
        'humidity': 78.60,
        'distance': 50.0,
        'weight': 0.0,
        'timestamp': int(time.time() * 1000)
    }
    
    print("📊 Sending sample data:")
    for key, value in sample_data.items():
        print(f"  {key}: {value}")
    
    if send_to_flask(sample_data):
        print("✅ Sample data sent successfully!")
        print("🔄 Now refreshing web page...")
        print("Go to http://localhost:5000/serial-config to see the data")
    
    print("\n💡 To send live data:")
    print("1. Copy ESP32 output from Serial Monitor")
    print("2. Paste it here and press Enter")
    print("3. Data will be parsed and sent to Flask")
    print("4. Or press Enter to send sample data again")
    
    try:
        while True:
            user_input = input("\n📝 Paste ESP32 data (or Enter for sample): ").strip()
            
            if user_input:
                # Parse the pasted data
                data = parse_esp32_data(user_input)
                print("📊 Parsed data:")
                for key, value in data.items():
                    print(f"  {key}: {value}")
                
                send_to_flask(data)
            else:
                # Send sample data
                sample_data['timestamp'] = int(time.time() * 1000)
                print("📊 Sending sample data...")
                send_to_flask(sample_data)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 ESP32 Data Bridge stopped")

if __name__ == "__main__":
    main()
