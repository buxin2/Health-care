#!/usr/bin/env python3
"""
Manual serial test - reads from ESP32 and shows raw data
"""

import serial
import requests
import time
import sys

def manual_serial_test(port_name):
    """Manually read from ESP32 and test data parsing"""
    print(f"🔌 Connecting to {port_name}...")
    
    try:
        ser = serial.Serial(port_name, 115200, timeout=1)
        print("✅ Connected! Reading data...")
        print("Press Ctrl+C to stop\n")
        
        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        print(f"📨 Raw: {line}")
                        
                        # Test parsing
                        if line.startswith('SENSOR_DATA:'):
                            print("🎯 Parsing sensor data...")
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
                                
                                print("📊 Parsed data:")
                                for key, value in sensor_data.items():
                                    print(f"  {key}: {value}")
                                
                                # Test sending to Flask
                                try:
                                    response = requests.post('http://localhost:5000/sensor-data', 
                                                           json=sensor_data, timeout=2)
                                    if response.status_code == 200:
                                        print("✅ Data sent to Flask successfully!")
                                    else:
                                        print(f"❌ Flask error: {response.status_code}")
                                except Exception as e:
                                    print(f"❌ Flask connection error: {e}")
                                
                                print("-" * 50)
                            else:
                                print(f"❌ Invalid data format: {len(values)} values")
                
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopped by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
        
        ser.close()
        print("🔌 Connection closed")
        
    except serial.SerialException as e:
        print(f"❌ Serial error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python manual_serial_test.py <COM_PORT>")
        print("Example: python manual_serial_test.py COM3")
        sys.exit(1)
    
    port = sys.argv[1]
    manual_serial_test(port)


