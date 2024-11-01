from flask import Blueprint
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Employee, OnboardingDocument, WelcomeEmail, Policy

serializer_bp = Blueprint('serializer_bp', __name__)
ma = Marshmallow(serializer_bp)

class OnboardingDocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OnboardingDocument
        include_fk = True 

    employee_id = fields.UUID(required=True)
    document_type = fields.String(required=True)
    document_path = fields.String(required=True)

onboarding_document_schema = OnboardingDocumentSchema()

class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_fk = True 
        exclude = ('password',)  

    onboarding_documents = fields.Nested(OnboardingDocumentSchema, many=True)
    national_id_number = fields.String(required=True)
    kra_pin_number = fields.String(required=True)
    
    bank_name = fields.String(required=True)
    branch_name = fields.String(allow_none=True)  
    account_name = fields.String(required=True)
    account_number = fields.String(required=True) 

employee_schema = EmployeeSchema()

class WelcomeEmailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WelcomeEmail
        include_fk = True 

    employee_id = fields.UUID(required=True)
    subject = fields.String(required=True)
    body = fields.String(required=True)
    sent_at = fields.DateTime(allow_none=True)  
    opened_at = fields.DateTime(allow_none=True) 

welcome_email_schema = WelcomeEmailSchema()

class PolicySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        include_fk = True 

policy_schema = PolicySchema()
