from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_mail import Message
from app import db, mail
from app.models import Appointment, Doctor
from datetime import datetime

main = Blueprint('main', __name__)


def send_email(to, subject, body):
    try:
        msg = Message(subject, recipients=[to], body=body)
        mail.send(msg)
    except Exception:
        pass


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/dashboard')
@login_required
def dashboard():
    appointments = Appointment.query.filter_by(
        patient_id=current_user.id
    ).order_by(Appointment.date.desc()).all()
    return render_template('main/dashboard.html', appointments=appointments)


@main.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    doctors = Doctor.query.all()

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date_str = request.form.get('date')
        time = request.form.get('time')
        reason = request.form.get('reason')

        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        existing = Appointment.query.filter_by(
            doctor_id=doctor_id, date=date, time=time
        ).filter(Appointment.status != 'Cancelled').first()

        if existing:
            flash('That time slot is already booked. Please choose another.', 'danger')
            return redirect(url_for('main.book'))

        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor_id,
            date=date,
            time=time,
            reason=reason
        )
        db.session.add(appointment)
        db.session.commit()

        doctor = Doctor.query.get(doctor_id)
        send_email(
            current_user.email,
            'Appointment Confirmation - City Clinic',
            f'Dear {current_user.full_name},\n\n'
            f'Your appointment has been booked.\n\n'
            f'Doctor: {doctor.name}\n'
            f'Date: {date_str}\n'
            f'Time: {time}\n'
            f'Reason: {reason}\n\n'
            f'Thank you for choosing City Clinic.'
        )

        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('main/book.html', doctors=doctors)


@main.route('/cancel/<int:appointment_id>')
@login_required
def cancel(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.patient_id != current_user.id:
        flash('Unauthorised action.', 'danger')
        return redirect(url_for('main.dashboard'))

    appointment.status = 'Cancelled'
    db.session.commit()

    flash('Appointment cancelled.', 'info')
    return redirect(url_for('main.dashboard'))