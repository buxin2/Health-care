from datetime import datetime
from .extensions import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    chief_complaint = db.Column(db.String(255), nullable=True)
    pain_level = db.Column(db.Integer, nullable=True)
    pain_description = db.Column(db.String(255), nullable=True)
    additional_symptoms = db.Column(db.String(255), nullable=True)
    medical_history = db.Column(db.String(255), nullable=True)
    emergency_name = db.Column(db.String(100), nullable=True)
    emergency_relation = db.Column(db.String(50), nullable=True)
    emergency_gender = db.Column(db.String(10), nullable=True)
    emergency_contact = db.Column(db.String(20), nullable=True)
    emergency_address = db.Column(db.String(255), nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)

    heart_rate = db.Column(db.Integer)
    spo2 = db.Column(db.Float)
    body_temperature = db.Column(db.Float)
    environment_temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class PatientHindi(db.Model):
    __tablename__ = 'patient_hindi'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    chief_complaint = db.Column(db.String(255), nullable=True)
    pain_level = db.Column(db.Integer, nullable=True)
    pain_description = db.Column(db.String(255), nullable=True)
    additional_symptoms = db.Column(db.String(255), nullable=True)
    medical_history = db.Column(db.String(255), nullable=True)
    emergency_name = db.Column(db.String(100), nullable=True)
    emergency_relation = db.Column(db.String(50), nullable=True)
    emergency_gender = db.Column(db.String(10), nullable=True)
    emergency_contact = db.Column(db.String(20), nullable=True)
    emergency_address = db.Column(db.String(255), nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    heart_rate = db.Column(db.Integer)
    spo2 = db.Column(db.Float)
    body_temperature = db.Column(db.Float)
    environment_temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


