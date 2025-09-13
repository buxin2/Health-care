import os
import time
import cv2
from flask import Response


# Global camera instance
_camera = None


def get_camera():
    """Get camera instance, create if needed"""
    global _camera
    if _camera is None or not _camera.isOpened():
        _camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not _camera.isOpened():
            _camera = cv2.VideoCapture(2)
    return _camera


def generate_frames():
    """Generate video frames for streaming"""
    while True:
        camera = get_camera()
        ret, frame = camera.read()
        
        if ret:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            time.sleep(0.1)


def capture_photo():
    """Capture a photo and save to uploads folder"""
    camera = get_camera()
    ret, frame = camera.read()
    
    if not ret:
        return None
    
    filename = f"captured_image_{int(time.time())}.jpg"
    os.makedirs('static/uploads', exist_ok=True)
    filepath = os.path.join('static/uploads', filename)
    cv2.imwrite(filepath, frame)
    return filename


def cleanup(exception=None):
    """Release camera resources"""
    global _camera
    if _camera:
        _camera.release()
        _camera = None