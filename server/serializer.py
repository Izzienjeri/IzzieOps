from flask import Blueprint
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Employee, EmployeeProfile, OnboardingDocument, Policy,AttendanceRecord

serializer_bp = Blueprint('serializer_bp', __name__)
ma = Marshmallow(serializer_bp)

class OnboardingDocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OnboardingDocument
        include_fk = True 

    document_type = fields.String(required=True)
    document_path = fields.String(required=True)
    submitted_at = fields.DateTime(allow_none=True) 
onboarding_document_schema = OnboardingDocumentSchema()

class EmployeeProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeProfile
        include_fk = True 

    position = fields.String(allow_none=True) 
    department = fields.String(allow_none=True) 
    bank_name = fields.String(allow_none=True) 
    branch_name = fields.String(allow_none=True) 
    account_name = fields.String(allow_none=True) 
    account_number = fields.String(allow_none=True)
    national_id_number = fields.String(allow_none=True) 
    kra_pin_number = fields.String(allow_none=True) 

employee_profile_schema = EmployeeProfileSchema()

class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_fk = True 
        exclude = ('password',)  # Exclude password for security reasons

    onboarding_documents = fields.Nested(OnboardingDocumentSchema, many=True)
    profile = fields.Nested(EmployeeProfileSchema, many=False)  # Nested profile schema

    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(allow_none=True) 

employee_schema = EmployeeSchema()


class PolicySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        include_fk = True 

    title = fields.String(required=True)
    content = fields.String(required=True)
    created_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)

policy_schema = PolicySchema()

class AttendanceRecordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AttendanceRecord
        include_fk = True

    employee_id = fields.String(required=True)
    clock_in_time = fields.DateTime(allow_none=True)
    clock_out_time = fields.DateTime(allow_none=True)
    break_start_time = fields.DateTime(allow_none=True)
    break_end_time = fields.DateTime(allow_none=True)
    total_hours_worked = fields.Float(allow_none=True)

attendance_record_schema = AttendanceRecordSchema()


