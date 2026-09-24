# Clinic Booking System

A full-stack medical appointment booking web application built with Flask and Bootstrap.

## Features
- Patient registration and secure login
- Book appointments with specialist doctors
- Patient dashboard to view and cancel appointments
- Admin dashboard with booking statistics
- Confirm or cancel appointments as admin
- Email confirmation on booking

## Tech Stack
Python | Flask | SQLAlchemy | SQLite | Bootstrap 5 | Flask-Login | Flask-Mail

## Project Structure
```
clinic-booking-system/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── main.py
│   ├── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── main/
│   │   └── admin/
│   └── static/
├── config.py
├── run.py
└── requirements.txt
```

## How to Run

1. Clone the repository:
```bash
   git clone https://github.com/LoloM-19/clinic-booking-system.git
   cd clinic-booking-system
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Run the application:
```bash
   python run.py
```

4. Open your browser at `http://127.0.0.1:5000`

## Default Admin Account
- **Email:** admin@cityclinic.com
- **Password:** admin123

## Sample Doctors Preloaded
- Dr. Sarah Johnson — General Practitioner
- Dr. Michael Chen — Cardiologist
- Dr. Aisha Patel — Dermatologist