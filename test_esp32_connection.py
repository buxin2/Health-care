#!/usr/bin/env python3
"""
Test script to check ESP32 serial communication
"""

import serial
import serial.tools.list_ports
import time
import sys

def list_available_ports():
    """List all available COM ports"""
    print("🔍 Available COM ports:")
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("  ❌ No COM ports found!")
        return []
    
    for i, port in enumerate(ports, 1):
        print(f"  {i}. {port.device} - {port.description}")
    return ports

def test_esp32_connection(port_name):
    """Test connection to ESP32"""
    print(f"\n🔌 Testing connection to {port_name}...")
    
    try:
        # Open serial connection
        ser = serial.Serial(port_name, 115200, timeout=5)
        print(f"  ✅ Connected to {port_name}")
        
        # Wait a moment for ESP32 to initialize
        time.sleep(2)
        
        # Clear any existing data
        ser.flushInput()
        
        print("  📡 Listening for data (10 seconds)...")
        start_time = time.time()
        data_received = False
        
        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        print(f"  📨 Received: {line}")
                        data_received = True
                        
                        # Check if it's sensor data
                        if line.startswith('SENSOR_DATA:'):
                            print(f"  🎯 Found sensor data: {line}")
                except UnicodeDecodeError:
                    print("  ⚠️  Received non-UTF8 data")
            time.sleep(0.1)
        
        ser.close()
        
        if data_received:
            print("  ✅ Data received successfully!")
        else:
            print("  ❌ No data received")
            
    except serial.SerialException as e:
        print(f"  ❌ Serial connection error: {e}")
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")

def main():
    print("=== ESP32 Connection Test ===")
    
    # List available ports
    ports = list_available_ports()
    
    if not ports:
        print("\n❌ No COM ports found. Make sure your ESP32 is connected!")
        return
    
    # If only one port, use it automatically
    if len(ports) == 1:
        port = ports[0]
        print(f"\n🎯 Auto-selecting only available port: {port.device}")
        test_esp32_connection(port.device)
    else:
        # Let user choose
        try:
            choice = input(f"\nSelect port (1-{len(ports)}): ")
            port_index = int(choice) - 1
            if 0 <= port_index < len(ports):
                test_esp32_connection(ports[port_index].device)
            else:
                print("❌ Invalid selection")
        except (ValueError, KeyboardInterrupt):
            print("❌ Cancelled")

if __name__ == "__main__":
    main()


