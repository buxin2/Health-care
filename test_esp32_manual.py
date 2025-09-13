#!/usr/bin/env python3
"""
Manual ESP32 test - run this to test your ESP32
"""

import serial
import requests
import time
import sys

def test_esp32():
    print("🔌 ESP32 Manual Test")
    print("=" * 50)
    
    # List available ports
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    print("Available ports:")
    for i, port in enumerate(ports, 1):
        print(f"  {i}. {port.device} - {port.description}")
    
    if not ports:
        print("❌ No COM ports found!")
        return
    
    # Try to connect to COM11 (or let user choose)
    port_name = "COM11"  # Change this if your ESP32 is on a different port
    print(f"\n🔌 Trying to connect to {port_name}...")
    
    try:
        ser = serial.Serial(port_name, 115200, timeout=2)
        print("✅ Connected to ESP32!")
        print("📡 Reading data for 30 seconds...")
        print("Press Ctrl+C to stop early\n")
        
        start_time = time.time()
        sensor_data_count = 0
        
        while time.time() - start_time < 30:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"📨 {line}")
                        
                        # Check for sensor data
                        if line.startswith('SENSOR_DATA:'):
                            sensor_data_count += 1
                            print(f"🎯 Sensor data #{sensor_data_count} found!")
                            
                            # Parse the data
                            data_str = line.replace('SENSOR_DATA:', '')
                            values = data_str.split(',')
                            
                            if len(values) == 8:
                                print("📊 Parsed sensor values:")
                                print(f"  Heart Rate: {values[0]} BPM")
                                print(f"  SpO2: {values[1]}%")
                                print(f"  Body Temp: {values[2]}°C")
                                print(f"  Room Temp: {values[3]}°C")
                                print(f"  Humidity: {values[4]}%")
                                print(f"  Distance: {values[5]} cm")
                                print(f"  Weight: {values[6]} g")
                                print(f"  Timestamp: {values[7]}")
                                print("-" * 40)
                            
                            # Try to send to Flask
                            try:
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
                                
                                response = requests.post('http://localhost:5000/sensor-data', 
                                                       json=sensor_data, timeout=2)
                                if response.status_code == 200:
                                    print("✅ Data sent to Flask successfully!")
                                else:
                                    print(f"❌ Flask error: {response.status_code}")
                            except Exception as e:
                                print(f"❌ Flask error: {e}")
                
                except UnicodeDecodeError:
                    print("⚠️  Received non-UTF8 data")
                except Exception as e:
                    print(f"❌ Error processing data: {e}")
            
            time.sleep(0.1)
        
        ser.close()
        print(f"\n✅ Test completed! Found {sensor_data_count} sensor data packets")
        
        if sensor_data_count > 0:
            print("🎉 Your ESP32 is working correctly!")
            print("💡 You can now use the web interface at http://localhost:5000/serial-config")
        else:
            print("⚠️  No sensor data found. Check your ESP32 code.")
        
    except serial.SerialException as e:
        print(f"❌ Serial connection error: {e}")
        print("\n💡 Solutions:")
        print("1. Close Arduino IDE and Serial Monitor")
        print("2. Unplug and replug ESP32")
        print("3. Check if ESP32 is on a different COM port")
        print("4. Make sure ESP32 code is uploaded and running")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_esp32()


