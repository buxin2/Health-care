#!/usr/bin/env python3
"""
Serial Reader for ESP32 Medical Robot
Reads sensor data from ESP32 via USB serial and sends to Flask app
"""

import serial
import requests
import time
import sys
import argparse
from typing import Dict, Any

# Configuration
BAUD_RATE = 115200
FLASK_URL = 'http://localhost:5000/sensor-data'

def parse_sensor_data(line: str) -> Dict[str, Any]:
    """Parse sensor data from ESP32 serial output"""
    try:
        if line.startswith('SENSOR_DATA:'):
            # Remove the prefix and split by comma
            data_str = line.replace('SENSOR_DATA:', '')
            values = data_str.strip().split(',')
            
            if len(values) == 8:
                return {
                    'heart_rate': int(float(values[0])),
                    'spo2': int(float(values[1])),
                    'body_temperature': float(values[2]),
                    'environment_temperature': float(values[3]),
                    'humidity': float(values[4]),
                    'distance': float(values[5]),
                    'weight': float(values[6]),
                    'timestamp': int(values[7])
                }
    except (ValueError, IndexError) as e:
        print(f"Error parsing sensor data: {e}")
        print(f"Raw line: {line}")
    
    return None

def send_to_flask(data: Dict[str, Any]) -> bool:
    """Send sensor data to Flask app"""
    try:
        response = requests.post(FLASK_URL, json=data, timeout=5)
        if response.status_code == 200:
            print(f"✓ Data sent to Flask: HR={data['heart_rate']}, SpO2={data['spo2']}, Temp={data['body_temperature']:.1f}°C")
            return True
        else:
            print(f"✗ Flask error: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
        return False

def main():
    """Main serial reader loop"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='ESP32 Medical Robot Serial Reader')
    parser.add_argument('--port', required=True, help='Serial port (e.g., COM3, /dev/ttyUSB0)')
    args = parser.parse_args()
    
    serial_port = args.port
    
    print("=== ESP32 Medical Robot Serial Reader ===")
    print(f"Serial Port: {serial_port}")
    print(f"Baud Rate: {BAUD_RATE}")
    print(f"Flask URL: {FLASK_URL}")
    print("Connecting to ESP32...")
    
    try:
        # Open serial connection
        ser = serial.Serial(serial_port, BAUD_RATE, timeout=1)
        print("✓ Connected to ESP32")
        print("Reading sensor data...\n")
        
        while True:
            try:
                # Read line from serial
                line = ser.readline().decode('utf-8').strip()
                
                if line:
                    # Parse and send sensor data
                    sensor_data = parse_sensor_data(line)
                    if sensor_data:
                        send_to_flask(sensor_data)
                    else:
                        # Print other serial output for debugging
                        if not line.startswith('SENSOR_DATA:'):
                            print(f"ESP32: {line}")
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except KeyboardInterrupt:
                print("\n\nStopping serial reader...")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)
    
    except serial.SerialException as e:
        print(f"✗ Serial connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if ESP32 is connected via USB")
        print("2. Verify the correct COM port (check Device Manager on Windows)")
        print("3. Make sure no other program is using the serial port")
        print("4. Try different COM ports: COM3, COM4, COM5, etc.")
        sys.exit(1)
    
    finally:
        if 'ser' in locals():
            ser.close()
            print("Serial connection closed")

if __name__ == "__main__":
    main()
