from typing import Dict, Any


_latest_data: Dict[str, Any] = {
    'heart_rate': 0,
    'spo2': 0,
    'body_temperature': 0,
    'environment_temperature': 0,
    'humidity': 0,
    'distance': 0,
    'weight': 0,
    'timestamp': 0
}


def update_sensor_data(data: Dict[str, Any]) -> None:
    global _latest_data
    _latest_data['heart_rate'] = data.get('heart_rate', _latest_data['heart_rate'])
    _latest_data['spo2'] = data.get('spo2', _latest_data['spo2'])
    _latest_data['body_temperature'] = data.get('body_temperature', _latest_data['body_temperature'])
    _latest_data['environment_temperature'] = data.get('environment_temperature', _latest_data['environment_temperature'])
    _latest_data['humidity'] = data.get('humidity', _latest_data['humidity'])
    _latest_data['distance'] = data.get('distance', _latest_data['distance'])
    _latest_data['weight'] = data.get('weight', _latest_data['weight'])
    _latest_data['timestamp'] = data.get('timestamp', _latest_data['timestamp'])


def update_servo_angles(servo1: int, servo2: int) -> None:
    global _latest_data
    _latest_data['servo1_angle'] = int(servo1)
    _latest_data['servo2_angle'] = int(servo2)


def get_latest_data() -> Dict[str, Any]:
    return _latest_data


