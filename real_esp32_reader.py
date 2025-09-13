#!/usr/bin/env python3
"""
Simple ESP32 Real Data Reader
Reads actual sensor data from ESP32 and sends to Flask
"""

import serial
import requests
import time
import re

def parse_esp32_line(line):
    """Parse ESP32 output to extract real sensor values"""
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
    
    # Extract room temperature
    if 'Room Temp:' in line:
        match = re.search(r'Room Temp: ([\d.]+)', line)
        if match:
            data['environment_temperature'] = float(match.group(1))
    
    # Extract humidity
    if 'Humidity:' in line:
        match = re.search(r'Humidity: ([\d.]+)', line)
        if match:
            data['humidity'] = float(match.group(1))
    
    # Extract body temperature
    if 'Temperature:' in line:
        match = re.search(r'Temperature: ([\d.]+)', line)
        if match:
            data['body_temperature'] = float(match.group(1))
    
    # Extract distance
    if 'Distance:' in line:
        match = re.search(r'Distance: ([\d.]+)', line)
        if match:
            data['distance'] = float(match.group(1))
    
    # Extract weight
    if 'Weight:' in line and 'grams' in line:
        match = re.search(r'Weight: ([\d.]+)', line)
        if match:
            data['weight'] = float(match.group(1))
    
    # Extract heart rate
    if 'Heart Rate:' in line and 'BPM' in line:
        match = re.search(r'Heart Rate: ([\d.]+)', line)
        if match:
            data['heart_rate'] = int(float(match.group(1)))
    
    # Extract SpO2
    if 'SpO2:' in line and '%' in line:
        match = re.search(r'SpO2: ([\d.]+)', line)
        if match:
            data['spo2'] = int(float(match.group(1)))
    
    return data

def send_to_flask(data):
    """Send data to Flask app"""
    try:
        response = requests.post('http://localhost:5000/sensor-data', json=data, timeout=2)
        if response.status_code == 200:
            print("✅ Data sent to Flask")
            return True
    except:
        pass
    return False

def main():
    print("🔌 ESP32 Real Data Reader")
    print("=" * 40)
    print("Reading actual sensor data from ESP32")
    print("Press Ctrl+C to stop")
    print()
    
    # Find ESP32 port
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("❌ No COM ports found!")
        return
    
    # Use first available port (usually COM11)
    port = ports[0].device
    print(f"🔌 Using port: {port}")
    
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print("✅ Connected to ESP32")
        print("📡 Reading sensor data...")
        print()
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"📨 {line}")
                    
                    # Parse sensor data
                    data = parse_esp32_line(line)
                    
                    # Send to Flask if we have data
                    if any(data[key] != 0 for key in ['body_temperature', 'environment_temperature', 'humidity', 'distance', 'weight']):
                        print(f"📊 Sending: Temp={data['body_temperature']}°C, Room={data['environment_temperature']}°C, Humidity={data['humidity']}%")
                        send_to_flask(data)
                        print()
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
