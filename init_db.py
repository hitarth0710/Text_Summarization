from app import create_app, db
from app.models import User, Summary

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created.")

    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('adminpassword')  # Change this in production!
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    print("Database initialized successfully!")