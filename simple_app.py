#!/usr/bin/env python3
"""
Simple Flask app without serial blueprint for testing
"""

from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Simple sensor data storage
sensor_data = {
    'heart_rate': 0,
    'spo2': 0,
    'body_temperature': 0,
    'environment_temperature': 0,
    'humidity': 0,
    'distance': 0,
    'weight': 0,
    'timestamp': 0
}

@app.route('/')
def home():
    return "Flask app is running! Go to /serial-config"

@app.route('/serial-config')
def serial_config():
    return render_template('serial-config.html')

@app.route('/latest')
def get_latest():
    return jsonify(sensor_data)

@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    global sensor_data
    data = request.get_json()
    if data:
        sensor_data.update(data)
        print(f"Received sensor data: {data}")
    return jsonify({"status": "success"})

# Add missing routes for template compatibility
@app.route('/dashboard')
def dashboard():
    return "Dashboard page - sensor data: " + str(sensor_data)

@app.route('/qa')
def qa():
    return "QA page"

@app.route('/patient_reviw')
def patient_review():
    return "Patient review page"

# Add API endpoints for serial reader
@app.route('/api/ports')
def get_ports():
    """Get list of available COM ports"""
    try:
        import serial.tools.list_ports
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'description': port.description,
                'hwid': port.hwid
            })
        return jsonify({'ports': ports})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start-serial-reader', methods=['POST'])
def start_serial_reader():
    """Start the serial reader with selected port"""
    try:
        data = request.get_json()
        port = data.get('port')
        
        if not port:
            return jsonify({'error': 'No port selected'}), 400
        
        # For now, just return success - the actual serial reading will be done by the bridge script
        return jsonify({
            'status': 'started',
            'port': port,
            'message': 'Serial reader started. Run python esp32_to_flask.py to send data.'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop-serial-reader', methods=['POST'])
def stop_serial_reader():
    """Stop the serial reader"""
    try:
        return jsonify({'status': 'stopped', 'message': 'Serial reader stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting simple Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
