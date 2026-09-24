from app import create_app, db
from app.models import User, Doctor

app = create_app()

with app.app_context():
    db.create_all()

    # Create default admin account
    if not User.query.filter_by(email='admin@cityclinic.com').first():
        admin = User(full_name='Admin', email='admin@cityclinic.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)

    # Create sample doctors
    if not Doctor.query.first():
        doctors = [
            Doctor(name='Sarah Johnson', specialization='General Practitioner'),
            Doctor(name='Michael Chen', specialization='Cardiologist'),
            Doctor(name='Aisha Patel', specialization='Dermatologist'),
        ]
        db.session.add_all(doctors)

    db.session.commit()
    print("Database initialised successfully.")

if __name__ == '__main__':
    app.run(debug=True)