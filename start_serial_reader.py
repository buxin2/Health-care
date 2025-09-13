#!/usr/bin/env python3
"""
Start serial reader for ESP32 - run this manually
"""

import serial
import requests
import time
import sys

def start_serial_reader():
    print("🔌 Starting ESP32 Serial Reader")
    print("=" * 50)
    
    try:
        # Connect to ESP32
        ser = serial.Serial('COM11', 115200, timeout=1)
        print("✅ Connected to ESP32 on COM11")
        print("📡 Reading sensor data...")
        print("Press Ctrl+C to stop\n")
        
        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"📨 {line}")
                        
                        # Check for sensor data
                        if line.startswith('SENSOR_DATA:'):
                            print("🎯 Processing sensor data...")
                            
                            # Parse the data
                            data_str = line.replace('SENSOR_DATA:', '')
                            values = data_str.split(',')
                            
                            if len(values) == 8:
                                sensor_data = {
                                    'heart_rate': int(float(values[0])),
                                    'spo2': int(float(values[1])),
                                    'body_temperature': float(values[2]),
                                    'environment_temperature': float(values[3]),
                                    'humidity': float(values[4]),
                                    'distance': float(values[5]),
                                    'weight': float(values[6]),
                                    'timestamp': int(values[7])
                                }
                                
                                print("📊 Sending to Flask:")
                                for key, value in sensor_data.items():
                                    print(f"  {key}: {value}")
                                
                                # Send to Flask
                                try:
                                    response = requests.post('http://localhost:5000/sensor-data', 
                                                           json=sensor_data, timeout=2)
                                    if response.status_code == 200:
                                        print("✅ Data sent to Flask successfully!")
                                    else:
                                        print(f"❌ Flask error: {response.status_code}")
                                except Exception as e:
                                    print(f"❌ Flask error: {e}")
                                
                                print("-" * 40)
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping serial reader...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
        
        ser.close()
        print("🔌 Serial reader stopped")
        
    except serial.SerialException as e:
        print(f"❌ Serial error: {e}")
        print("\n💡 Solutions:")
        print("1. Close Arduino IDE and Serial Monitor")
        print("2. Unplug and replug ESP32")
        print("3. Make sure ESP32 is on COM11")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    start_serial_reader()


