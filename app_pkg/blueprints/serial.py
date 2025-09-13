from flask import Blueprint, render_template, jsonify, request
import serial.tools.list_ports
import subprocess
import sys
import os

serial_bp = Blueprint('serial', __name__)

@serial_bp.route('/serial-config')
def serial_config():
    """Port selection page"""
    return render_template('serial-config.html')

@serial_bp.route('/api/ports')
def get_ports():
    """Get list of available COM ports"""
    try:
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

@serial_bp.route('/api/start-serial-reader', methods=['POST'])
def start_serial_reader():
    """Start the serial reader with selected port"""
    try:
        data = request.get_json()
        port = data.get('port')
        
        if not port:
            return jsonify({'error': 'No port selected'}), 400
        
        # Start serial reader as subprocess
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'serial_reader.py')
        
        # Use the same Python interpreter that's running Flask
        python_exe = sys.executable
        
        # Start the process
        process = subprocess.Popen([
            python_exe, script_path, '--port', port
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return jsonify({
            'status': 'started',
            'port': port,
            'pid': process.pid
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@serial_bp.route('/api/stop-serial-reader', methods=['POST'])
def stop_serial_reader():
    """Stop the serial reader"""
    try:
        # Find and kill the serial reader process
        if sys.platform == 'win32':
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
        else:
            subprocess.run(['pkill', '-f', 'serial_reader.py'], 
                         capture_output=True, text=True)
        
        return jsonify({'status': 'stopped'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
