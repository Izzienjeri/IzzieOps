from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    onboarding_documents = db.relationship('OnboardingDocument', backref='employee', lazy=True)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

class OnboardingDocument(db.Model):
    __tablename__ = 'onboarding_documents'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)  # e.g., 'ID', 'Contract'
    document_path = db.Column(db.String(255), nullable=False)  # Path to the uploaded document
    submitted_at = db.Column(db.DateTime, nullable=False)  # Timestamp for when the document was submitted

    def __repr__(self):
        return f'<OnboardingDocument {self.document_type} for Employee ID {self.employee_id}>'

class WelcomeEmail(db.Model):
    __tablename__ = 'welcome_emails'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)  # Timestamp for when the email was sent

    def __repr__(self):
        return f'<WelcomeEmail for Employee ID {self.employee_id}>'

class Policy(db.Model):
    __tablename__ = 'policies'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)  # The full content of the policy
    created_at = db.Column(db.DateTime, nullable=False)  # When the policy was created
    updated_at = db.Column(db.DateTime, nullable=True)  # When the policy was last updated

    def __repr__(self):
        return f'<Policy {self.title}>'
