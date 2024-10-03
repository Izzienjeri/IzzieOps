import uuid
from sqlalchemy import Enum, MetaData
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import re

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
    manager_id = db.Column(db.String(36), db.ForeignKey('managers.id'), nullable=True)
    
    documents = db.relationship('Document', backref='employee', lazy=True)
    tasks = db.relationship('Task', backref='employee', lazy=True)
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy=True)

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"

class Manager(Employee):
    __tablename__ = 'managers'
    
    id = db.Column(db.String(36), db.ForeignKey('employees.id'), primary_key=True)

    def __repr__(self):
        return f"<Manager {self.first_name} {self.last_name}>"

    def approve_leave_request(self, leave_request):
        leave_request.status = LeaveRequestStatusEnum.APPROVED
        leave_request.approver_id = self.id
        db.session.commit()

    def reject_leave_request(self, leave_request):
        leave_request.status = LeaveRequestStatusEnum.REJECTED
        leave_request.approver_id = self.id
        db.session.commit()

class Admin(Employee):
    __tablename__ = 'admins'
    
    id = db.Column(db.String(36), db.ForeignKey('employees.id'), primary_key=True)

    def __repr__(self):
        return f"<Admin {self.first_name} {self.last_name}>"

    def create_employee(self, first_name, last_name, email, position):
        new_employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            position=position
        )
        db.session.add(new_employee)
        db.session.commit()
        return new_employee

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)

    @validates('document_type')
    def validate_document_type(self, key, document_type):
        allowed_types = ['PDF', 'DOCX', 'JPEG', 'PNG']
        if document_type not in allowed_types:
            raise ValueError(f"Document type must be one of: {', '.join(allowed_types)}")
        return document_type

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

    @validates('due_date')
    def validate_due_date(self, key, due_date):
        if due_date < db.func.current_date():
            raise ValueError("Due date must be in the future")
        return due_date

    def send_notification(self):
        notification = Notification(
            employee_id=self.employee_id,
            type=NotificationTypeEnum.TASK_ASSIGNED,
            message=f"Task '{self.title}' has been assigned to you."
        )
        db.session.add(notification)
        db.session.commit()

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
    approver_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=True)

    @validates('status')
    def validate_leave_status(self, key, value):
        if value not in LeaveRequestStatusEnum:
            raise ValueError("Invalid leave request status value")
        return value

    @validates('start_date', 'end_date')
    def validate_dates(self, key, date):
        if key == 'end_date' and date < self.start_date:
            raise ValueError("End date must be after start date")
        return date

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

    @validates('pay_period_end')
    def validate_pay_period(self, key, pay_period_end):
        if pay_period_end < self.pay_period_start:
            raise ValueError("Pay period end date must be after start date")
        return pay_period_end

    def __repr__(self):
        return f"<Payroll for Employee ID {self.employee_id} on {self.pay_date}>"

class NotificationTypeEnum(Enum):
    TASK_ASSIGNED = "task_assigned"
    LEAVE_REQUEST = "leave_request"

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    employee_id = db.Column(db.String(36), db.ForeignKey('employees.id'), nullable=False)
    type = db.Column(Enum(NotificationTypeEnum), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)  # Track whether the notification has been read
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Notification {self.type} for Employee ID {self.employee_id}>"
