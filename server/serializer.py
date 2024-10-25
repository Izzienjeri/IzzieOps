from flask import Blueprint
from marshmallow import validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import db, Employee, Manager, Admin, Document, Task, Attendance, LeaveRequest, Payroll, Notification

serializer_bp = Blueprint('serializer_bp', __name__)

class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        include_relationships = True  

class ManagerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Manager
        load_instance = True
        include_relationships = True

class AdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        load_instance = True
        include_relationships = True

class DocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        load_instance = True

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True

class AttendanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
        load_instance = True

class LeaveRequestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LeaveRequest
        load_instance = True

class PayrollSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Payroll
        load_instance = True

class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True

# Example of a custom validation
class EmployeeRegisterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        exclude = ('id',)  # Exclude ID for registration

    @validates('email')
    def validate_email(self, email):
        if Employee.query.filter_by(email=email).first():
            raise ValidationError("Email already exists")

# Exporting the schemas for use in your routes or services
__all__ = [
    'EmployeeSchema',
    'ManagerSchema',
    'AdminSchema',
    'DocumentSchema',
    'TaskSchema',
    'AttendanceSchema',
    'LeaveRequestSchema',
    'PayrollSchema',
    'NotificationSchema',
    'EmployeeRegisterSchema'
]
