#!/usr/bin/env python3
"""
Quick test to check ESP32 communication
"""

import serial
import time

def quick_test():
    print("🔌 Quick ESP32 Test")
    print("Available ports:")
    
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(f"  - {port.device}: {port.description}")
    
    if not ports:
        print("❌ No ports found!")
        return
    
    # Try COM11 (from earlier detection)
    port_name = "COM11"
    print(f"\n🔌 Trying to connect to {port_name}...")
    
    try:
        ser = serial.Serial(port_name, 115200, timeout=2)
        print("✅ Connected!")
        
        # Wait for data
        print("📡 Waiting for data (5 seconds)...")
        start_time = time.time()
        
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    print(f"📨 {line}")
                    if "SENSOR_DATA:" in line:
                        print("🎯 Found sensor data!")
                        break
            time.sleep(0.1)
        
        ser.close()
        print("✅ Test completed")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Try:")
        print("1. Close Arduino IDE")
        print("2. Close Serial Monitor")
        print("3. Unplug and replug ESP32")
        print("4. Try again")

if __name__ == "__main__":
    quick_test()


