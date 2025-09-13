from flask import Blueprint, redirect, url_for, render_template


pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def root():
    return redirect(url_for('pages.qa'))


@pages_bp.route('/patient-details.html')
def patient_details_page():
    return render_template('patient-details.html')


@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@pages_bp.route('/qa')
def qa():
    return render_template('qa.html')


@pages_bp.route('/patient_reviw')
def patient_reviw():
    return render_template('patient_reviw.html')


 



