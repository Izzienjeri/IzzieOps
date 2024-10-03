import uuid
from sqlalchemy import Enum, MetaData
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(metadata=MetaData())

def generate_uuid():
    return str(uuid.uuid4())

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    manager_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=True)
    documents = db.relationship('Document', backref='employee', lazy=True)
    tasks = db.relationship('Task', backref='employee', lazy=True)
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy=True)

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Document {self.document_type} for Employee ID {self.employee_id}>"

class TaskStatusEnum(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(Enum(TaskStatusEnum), default=TaskStatusEnum.PENDING)
    due_date = db.Column(db.Date, nullable=False)

    @validates('status')
    def validate_status(self, key, value):
        if value not in TaskStatusEnum:
            raise ValueError("Invalid status value")
        return value

    def __repr__(self):
        return f"<Task {self.title} for Employee ID {self.employee_id}>"

class AttendanceStatusEnum(Enum):
    WORKING = "working"
    ON_BREAK = "on_break"
    OFF = "off"

class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    clock_in_time = db.Column(db.DateTime, nullable=False)
    clock_out_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(Enum(AttendanceStatusEnum), default=AttendanceStatusEnum.WORKING)

    @validates('status')
    def validate_attendance_status(self, key, value):
        if value not in AttendanceStatusEnum:
            raise ValueError("Invalid attendance status value")
        return value

    def __repr__(self):
        return f"<Attendance for Employee ID {self.employee_id} on {self.clock_in_time}>"

class LeaveRequestStatusEnum(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(Enum(LeaveRequestStatusEnum), default=LeaveRequestStatusEnum.PENDING)

    @validates('status')
    def validate_leave_status(self, key, value):
        if value not in LeaveRequestStatusEnum:
            raise ValueError("Invalid leave request status value")
        return value

    def __repr__(self):
        return f"<LeaveRequest {self.leave_type} for Employee ID {self.employee_id}>"

class Payroll(db.Model):
    __tablename__ = 'payrolls'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    pay_date = db.Column(db.Date, nullable=False)
    pay_period_start = db.Column(db.Date, nullable=False)
    pay_period_end = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Payroll for Employee ID {self.employee_id} on {self.pay_date}>"
