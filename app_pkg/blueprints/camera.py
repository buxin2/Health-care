from flask import Blueprint, Response, jsonify
from ..services import camera as cam
from ..models import Patient
from ..extensions import db


camera_bp = Blueprint('camera', __name__)


@camera_bp.route('/video_feed')
def video_feed():
    """Live video stream"""
    return Response(cam.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@camera_bp.route('/take_picture')
def take_picture():
    """Capture photo and save to database"""
    filename = cam.capture_photo()
    
    if filename:
        # Save to latest patient
        try:
            last_patient = Patient.query.order_by(Patient.id.desc()).first()
            if last_patient:
                last_patient.photo_filename = filename
                db.session.commit()
        except Exception:
            pass
        
        return jsonify({"status": "success", "filename": filename})
    
    return jsonify({"status": "error", "message": "Failed to capture photo"})