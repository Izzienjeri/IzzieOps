# seed.py
import uuid
from datetime import datetime
from extensions import db
from models import Employee, OnboardingDocument, WelcomeEmail, Policy
from app import create_app

app = create_app()

def seed_data():
    with app.app_context():
        # Check if employees already exist
        existing_employees = db.session.query(Employee).filter(Employee.email.in_(["john.doe@example.com", "jane.smith@example.com"])).all()
        existing_emails = {emp.email for emp in existing_employees}

        # Seed Employees if they don't exist
        if "john.doe@example.com" not in existing_emails:
            employee1 = Employee(
                id=str(uuid.uuid4()),
                first_name='John',
                last_name='Doe',
                email='john.doe@example.com',
                phone='1234567890',
                position='Software Engineer',
                department='Engineering',
                password='securepassword'
            )
            db.session.add(employee1)

        if "jane.smith@example.com" not in existing_emails:
            employee2 = Employee(
                id=str(uuid.uuid4()),
                first_name='Jane',
                last_name='Smith',
                email='jane.smith@example.com',
                phone='0987654321',
                position='Product Manager',
                department='Product',
                password='securepassword'
            )
            db.session.add(employee2)

        # Commit to save the new employees if any
        db.session.commit()

        # Seed Onboarding Documents for existing employees
        for emp in existing_employees:
            if not db.session.query(OnboardingDocument).filter_by(employee_id=emp.id).count():  # Check if any docs exist for the employee
                doc1 = OnboardingDocument(
                    employee_id=emp.id,
                    document_type='Employment Contract',
                    document_path='path/to/contract.pdf',
                    submitted_at=datetime.utcnow()
                )

                doc2 = OnboardingDocument(
                    employee_id=emp.id,
                    document_type='Tax Forms',
                    document_path='path/to/tax_forms.pdf',
                    submitted_at=datetime.utcnow()
                )

                db.session.add(doc1)
                db.session.add(doc2)

        # Seed Welcome Emails for existing employees
        for emp in existing_employees:
            if not db.session.query(WelcomeEmail).filter_by(employee_id=emp.id).count():  # Check if any emails sent for the employee
                welcome_email = WelcomeEmail(
                    employee_id=emp.id,
                    subject='Welcome to the Team!',
                    body=f'Hello {emp.first_name}, welcome to our company!',
                    sent_at=datetime.utcnow()
                )
                db.session.add(welcome_email)

        # Seed Policies if not already existing
        if not db.session.query(Policy).count():  # Check if policies exist
            policy1 = Policy(
                title='Company Code of Conduct',
                content='All employees are expected to adhere to the company code of conduct.',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            policy2 = Policy(
                title='Leave Policy',
                content='Employees are entitled to paid leave under certain conditions.',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.session.add(policy1)
            db.session.add(policy2)

        # Commit the session
        db.session.commit()
        print("Data seeded successfully!")

if __name__ == '__main__':
    seed_data()
