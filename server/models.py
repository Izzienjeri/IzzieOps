from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=True)  
    position = db.Column(db.String(150), nullable=True, default=None)  
    department = db.Column(db.String(150), nullable=True, default=None)  

    password = db.Column(db.String(256), nullable=False)  

    onboarding_documents = db.relationship('OnboardingDocument', backref='employee', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name} - {self.email}>'

    
class EmployeeProfile(db.Model):
    __tablename__ = 'employee_profiles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    position = db.Column(db.String(150), nullable=True) 
    department = db.Column(db.String(150), nullable=True) 
    bank_name = db.Column(db.String(150), nullable=True) 
    branch_name = db.Column(db.String(150), nullable=True) 
    account_name = db.Column(db.String(150), nullable=True) 
    account_number = db.Column(db.String(30), nullable=True) 

    employee = db.relationship("Employee", backref=db.backref("profile", uselist=False))    

    def __repr__(self):
        return f'<EmployeeProfile for Employee ID {self.employee_id}>'
    

class OnboardingDocument(db.Model):
    __tablename__ = 'onboarding_documents'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    document_type = db.Column(db.String(150), nullable=False) 
    document_path = db.Column(db.String(500), nullable=False) 
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OnboardingDocument {self.document_type} for Employee ID {self.employee_id}>'

class WelcomeEmail(db.Model):
    __tablename__ = 'welcome_emails'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)  
    body = db.Column(db.Text, nullable=False)  
    sent_at = db.Column(db.DateTime, nullable=True)
    opened_at = db.Column(db.DateTime, nullable=True)  

    def __repr__(self):
        return f'<WelcomeEmail for Employee ID {self.employee_id}>'

class Policy(db.Model):
    __tablename__ = 'policies'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)  
    content = db.Column(db.Text, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Policy {self.title}>'
