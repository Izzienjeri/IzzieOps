# remove_data.py
from extensions import db
from models import Employee, OnboardingDocument, WelcomeEmail, Policy
from app import create_app

app = create_app()

def remove_data():
    with app.app_context():
        # Remove Onboarding Documents
        db.session.query(OnboardingDocument).delete()
        
        # Remove Welcome Emails
        db.session.query(WelcomeEmail).delete()

        # Remove Policies
        db.session.query(Policy).delete()

        # Remove Employees
        db.session.query(Employee).delete()

        # Commit the changes to the database
        db.session.commit()
        print("Data removed successfully!")

if __name__ == '__main__':
    remove_data()
