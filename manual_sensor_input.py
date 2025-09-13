#!/usr/bin/env python3
"""
Manual Sensor Input - Enter real ESP32 values
Simple and clean code
"""

import requests
import time

def send_sensor_data():
    """Send sensor data to Flask"""
    print("📊 Enter your ESP32 sensor values:")
    print()
    
    # Get real values from user
    body_temp = float(input("Body Temperature (°C): "))
    room_temp = float(input("Room Temperature (°C): "))
    humidity = float(input("Humidity (%): "))
    distance = float(input("Distance (cm): "))
    weight = float(input("Weight (g): "))
    heart_rate = int(input("Heart Rate (BPM, 0 if no finger): "))
    spo2 = int(input("SpO2 (%, 0 if no finger): "))
    
    # Create data
    data = {
        'heart_rate': heart_rate,
        'spo2': spo2,
        'body_temperature': body_temp,
        'environment_temperature': room_temp,
        'humidity': humidity,
        'distance': distance,
        'weight': weight,
        'timestamp': int(time.time() * 1000)
    }
    
    print()
    print("📊 Sending data:")
    print(f"  Body Temp: {body_temp}°C")
    print(f"  Room Temp: {room_temp}°C")
    print(f"  Humidity: {humidity}%")
    print(f"  Distance: {distance} cm")
    print(f"  Weight: {weight} g")
    print(f"  Heart Rate: {heart_rate} BPM")
    print(f"  SpO2: {spo2}%")
    
    # Send to Flask
    try:
        response = requests.post('http://localhost:5000/sensor-data', json=data, timeout=2)
        if response.status_code == 200:
            print("✅ Data sent successfully!")
            print("🔄 Refresh your web page to see the values")
        else:
            print("❌ Error sending data")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔌 Manual ESP32 Sensor Input")
    print("=" * 40)
    print("Enter real sensor values from your ESP32")
    print()
    
    while True:
        try:
            send_sensor_data()
            print()
            again = input("Enter more data? (y/n): ").lower()
            if again != 'y':
                break
            print()
        except KeyboardInterrupt:
            print("\n🛑 Stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
