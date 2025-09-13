#!/usr/bin/env python3
"""
Quick check to see if ESP32 is sending data
"""

import serial
import time

def check_esp32():
    print("🔍 Checking ESP32 data...")
    
    try:
        # Try to connect to COM11
        ser = serial.Serial('COM11', 115200, timeout=1)
        print("✅ Connected to COM11")
        
        # Clear any existing data
        ser.flushInput()
        
        print("📡 Listening for 10 seconds...")
        start_time = time.time()
        data_found = False
        
        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"📨 {line}")
                        data_found = True
                        
                        if "SENSOR_DATA:" in line:
                            print("🎯 Found sensor data!")
                            break
                except:
                    pass
            time.sleep(0.1)
        
        ser.close()
        
        if data_found:
            print("✅ ESP32 is sending data!")
        else:
            print("❌ No data received from ESP32")
            print("💡 Check:")
            print("  1. Is ESP32 code uploaded?")
            print("  2. Is ESP32 powered on?")
            print("  3. Are sensors connected?")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_esp32()


