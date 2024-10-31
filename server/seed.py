# seed.py
from app import create_app
from extensions import db
from models import Employee, OnboardingDocument, WelcomeEmail, Policy

app = create_app()

def seed_data():
    with app.app_context():
        # Create sample employees
        employee1 = Employee(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            position='Software Engineer',
            department='Engineering',
        )
        employee1.set_password('password123')  # Set password
        
        employee2 = Employee(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='0987654321',
            position='Product Manager',
            department='Product',
        )
        employee2.set_password('password456')  # Set password

        # Add employees to the session
        db.session.add(employee1)
        db.session.add(employee2)

        # Commit the session to the database
        db.session.commit()

        # Create sample onboarding documents
        doc1 = OnboardingDocument(
            employee_id=employee1.id,
            document_type='Tax Form',
            document_path='/path/to/tax_form.pdf',
        )
        
        doc2 = OnboardingDocument(
            employee_id=employee2.id,
            document_type='ID Verification',
            document_path='/path/to/id_verification.pdf',
        )
        
        db.session.add(doc1)
        db.session.add(doc2)

        # Commit onboarding documents
        db.session.commit()

        # Create sample welcome emails
        welcome_email1 = WelcomeEmail(
            employee_id=employee1.id,
            subject='Welcome to the Team!',
            body='We are excited to have you on board, John!',
        )

        welcome_email2 = WelcomeEmail(
            employee_id=employee2.id,
            subject='Welcome to the Team!',
            body='We are excited to have you on board, Jane!',
        )

        db.session.add(welcome_email1)
        db.session.add(welcome_email2)

        # Commit welcome emails
        db.session.commit()

        # Create sample policies
        policy1 = Policy(
            title='Employee Handbook',
            content='This is the employee handbook covering company policies and procedures.',
        )

        policy2 = Policy(
            title='Code of Conduct',
            content='All employees are expected to adhere to the company code of conduct.',
        )

        db.session.add(policy1)
        db.session.add(policy2)

        # Commit policies
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
