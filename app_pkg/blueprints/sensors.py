from flask import Blueprint, jsonify, request
from ..services import sensors


sensors_bp = Blueprint('sensors', __name__)


@sensors_bp.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    sensors.update_sensor_data(data)
    return jsonify({"status": "success"}), 200


@sensors_bp.route('/set-servos', methods=['POST'])
def set_servos():
    data = request.get_json()
    sensors.update_servo_angles(int(data.get('servo1', 90)), int(data.get('servo2', 90)))
    return jsonify({"status": "updated"}), 200


@sensors_bp.route('/latest', methods=['GET'])
def get_latest():
    return jsonify(sensors.get_latest_data())



