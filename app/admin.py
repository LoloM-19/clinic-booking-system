from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import Appointment, User, Doctor

admin = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_appointments = Appointment.query.count()
    pending = Appointment.query.filter_by(status='Pending').count()
    confirmed = Appointment.query.filter_by(status='Confirmed').count()
    cancelled = Appointment.query.filter_by(status='Cancelled').count()
    total_patients = User.query.filter_by(is_admin=False).count()
    total_doctors = Doctor.query.count()
    recent_appointments = Appointment.query.order_by(
        Appointment.created_at.desc()
    ).limit(5).all()

    return render_template('admin/dashboard.html',
        total_appointments=total_appointments,
        pending=pending,
        confirmed=confirmed,
        cancelled=cancelled,
        total_patients=total_patients,
        total_doctors=total_doctors,
        recent_appointments=recent_appointments
    )


@admin.route('/appointments')
@login_required
@admin_required
def appointments():
    all_appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin/appointments.html', appointments=all_appointments)


@admin.route('/confirm/<int:appointment_id>')
@login_required
@admin_required
def confirm(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'Confirmed'
    db.session.commit()
    flash('Appointment confirmed.', 'success')
    return redirect(url_for('admin.appointments'))


@admin.route('/cancel/<int:appointment_id>')
@login_required
@admin_required
def cancel(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'Cancelled'
    db.session.commit()
    flash('Appointment cancelled.', 'info')
    return redirect(url_for('admin.appointments'))