import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.String(36), db.ForeignKey('employees.id'))
    
    # Relationship
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')

    def __repr__(self):
        return f'<Employee {self.name}>'

class DocumentSubmission(db.Model):
    __tablename__ = 'document_submissions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    document_url = db.Column(db.String(255), nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False)

    # Relationship
    employee = db.relationship('Employee', backref='documents')

    def __repr__(self):
        return f'<DocumentSubmission {self.document_type} by {self.employee.name}>'

class TimeEntry(db.Model):
    __tablename__ = 'time_entries'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    clock_in = db.Column(db.DateTime, nullable=False)
    clock_out = db.Column(db.DateTime)
    break_duration = db.Column(db.Float, default=0)

    # Relationship
    employee = db.relationship('Employee', backref='time_entries')

    def __repr__(self):
        return f'<TimeEntry {self.id} for {self.employee.name}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    assigned_to_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')

    # Relationship
    assigned_to = db.relationship('Employee', backref='tasks')

    def __repr__(self):
        return f'<Task {self.title} assigned to {self.assigned_to.name}>'

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='pending')

    # Relationship
    employee = db.relationship('Employee', backref='leave_requests')

    def __repr__(self):
        return f'<LeaveRequest {self.id} by {self.employee.name}>'

class Payroll(db.Model):
    __tablename__ = 'payrolls'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)

    # Relationship
    employee = db.relationship('Employee', backref='payrolls')

    def __repr__(self):
        return f'<Payroll for {self.employee.name} on {self.payment_date}>'

class Policy(db.Model):
    __tablename__ = 'policies'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Policy {self.title}>'

# Initialize the database (assuming you have app context setup elsewhere)
def create_db(app):
    with app.app_context():
        db.create_all()
