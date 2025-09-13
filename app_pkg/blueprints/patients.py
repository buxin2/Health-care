import csv
from io import StringIO
from flask import Blueprint, jsonify, request, make_response
from ..extensions import db
from ..models import Patient, PatientHindi


patients_bp = Blueprint('patients', __name__)


@patients_bp.route('/submit_patient_data', methods=['POST'])
def receive_patient_data():
    data = request.get_json()

    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        contact=data['contact'],
        address=data['address'],
        chief_complaint=data['chiefComplaint'],
        pain_level=data['painLevel'],
        pain_description=data['painDescription'],
        additional_symptoms=data['additionalSymptoms'],
        medical_history=data['medicalHistory'],
        emergency_name=data['emergencyName'],
        emergency_relation=data['emergencyRelation'],
        emergency_gender=data['emergencyGender'],
        emergency_contact=data['emergencyContact'],
        emergency_address=data['emergencyAddress'],
        photo_filename=data.get('photoFilename'),
        heart_rate=data.get('heart_rate'),
        spo2=data.get('spo2'),
        body_temperature=data.get('body_temperature'),
        environment_temperature=data.get('environment_temperature')
    )

    try:
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"status": "success", "message": "Patient + sensor data saved!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400


@patients_bp.route('/submit_patient_data_hi', methods=['POST'])
def receive_patient_data_hindi():
    data = request.get_json()

    new_patient = PatientHindi(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        contact=data['contact'],
        address=data['address'],
        chief_complaint=data['chiefComplaint'],
        pain_level=data['painLevel'],
        pain_description=data['painDescription'],
        additional_symptoms=data['additionalSymptoms'],
        medical_history=data['medicalHistory'],
        emergency_name=data['emergencyName'],
        emergency_relation=data['emergencyRelation'],
        emergency_gender=data['emergencyGender'],
        emergency_contact=data['emergencyContact'],
        emergency_address=data['emergencyAddress'],
        photo_filename=data.get('photoFilename'),
        heart_rate=data.get('heart_rate'),
        spo2=data.get('spo2'),
        body_temperature=data.get('body_temperature'),
        environment_temperature=data.get('environment_temperature')
    )

    try:
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"status": "success", "message": "Patient (Hindi) + sensor data saved!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400


@patients_bp.route('/get_patient/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "contact": patient.contact,
        "address": patient.address,
        "chiefComplaint": patient.chief_complaint,
        "painLevel": patient.pain_level,
        "painDescription": patient.pain_description,
        "additionalSymptoms": patient.additional_symptoms,
        "medicalHistory": patient.medical_history,
        "emergencyName": patient.emergency_name,
        "emergencyRelation": patient.emergency_relation,
        "emergencyGender": patient.emergency_gender,
        "emergencyContact": patient.emergency_contact,
        "emergencyAddress": patient.emergency_address,
        "photoFilename": patient.photo_filename,
        "heart_rate": patient.heart_rate,
        "spo2": patient.spo2,
        "body_temperature": patient.body_temperature,
        "environment_temperature": patient.environment_temperature
    })


@patients_bp.route('/patients')
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'age': p.age,
            'gender': p.gender,
            'contact': p.contact,
            'address': p.address,
            'chiefComplaint': p.chief_complaint,
            'painLevel': p.pain_level,
            'painDescription': p.pain_description,
            'additionalSymptoms': p.additional_symptoms,
            'medicalHistory': p.medical_history,
            'emergencyName': p.emergency_name,
            'emergencyRelation': p.emergency_relation,
            'emergencyGender': p.emergency_gender,
            'emergencyContact': p.emergency_contact,
            'emergencyAddress': p.emergency_address,
            'photoFilename': p.photo_filename,
            'heart_rate': p.heart_rate,
            'spo2': p.spo2,
            'body_temperature': p.body_temperature,
            'environment_temperature': p.environment_temperature
        } for p in patients
    ])


@patients_bp.route('/update_patient/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    patient = Patient.query.get_or_404(patient_id)

    try:
        patient.name = data['name']
        patient.age = data['age']
        patient.gender = data['gender']
        patient.contact = data['contact']
        patient.address = data['address']
        patient.chief_complaint = data['chiefComplaint']
        patient.pain_level = data['painLevel']
        patient.pain_description = data['painDescription']
        patient.additional_symptoms = data['additionalSymptoms']
        patient.medical_history = data['medicalHistory']
        patient.emergency_name = data['emergencyName']
        patient.emergency_relation = data['emergencyRelation']
        patient.emergency_gender = data['emergencyGender']
        patient.emergency_contact = data['emergencyContact']
        patient.emergency_address = data['emergencyAddress']
        if 'photoFilename' in data:
            patient.photo_filename = data['photoFilename']

        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Patient updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@patients_bp.route('/delete_patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'status': 'error', 'message': 'Patient not found'}), 404

    try:
        if patient.photo_filename:
            import os
            photo_path = os.path.join('static', 'uploads', patient.photo_filename)
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except Exception:
                    pass
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400


@patients_bp.route('/export_csv', methods=['GET'])
def export_csv():
    patients = Patient.query.all()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow([
        "ID", "Name", "Age", "Gender", "Contact", "Address",
        "Chief Complaint", "Pain Level", "Pain Description",
        "Additional Symptoms", "Medical History",
        "Emergency Name", "Emergency Relation", "Emergency Gender",
        "Emergency Contact", "Emergency Address", "Photo Filename"
    ])
    for p in patients:
        writer.writerow([
            p.id, p.name, p.age, p.gender, p.contact, p.address,
            p.chief_complaint, p.pain_level, p.pain_description,
            p.additional_symptoms, p.medical_history,
            p.emergency_name, p.emergency_relation, p.emergency_gender,
            p.emergency_contact, p.emergency_address,
            p.photo_filename
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=patients.csv"
    output.headers["Content-type"] = "text/csv"
    return output



