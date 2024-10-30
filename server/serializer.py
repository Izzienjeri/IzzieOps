# serializer.py
from flask import Blueprint
from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Employee, OnboardingDocument, WelcomeEmail, Policy

# Create a Blueprint for serializers
serializer_bp = Blueprint('serializer_bp', __name__)
ma = Marshmallow(serializer_bp)


# OnboardingDocument Schema
class OnboardingDocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OnboardingDocument
        include_fk = True  # Include foreign keys

    employee_id = fields.UUID(required=True)
    document_type = fields.String(required=True)
    document_path = fields.String(required=True)

onboarding_document_schema = OnboardingDocumentSchema()

# Employee Schema
class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_fk = True  # Include foreign keys
        exclude = ('password',)  # Exclude password for security

    onboarding_documents = fields.Nested(OnboardingDocumentSchema, many=True)

employee_schema = EmployeeSchema()

# WelcomeEmail Schema
class WelcomeEmailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WelcomeEmail
        include_fk = True  # Include foreign keys

    employee_id = fields.UUID(required=True)
    subject = fields.String(required=True)
    body = fields.String(required=True)

welcome_email_schema = WelcomeEmailSchema()

# Policy Schema
class PolicySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        include_fk = True  # Include foreign keys

policy_schema = PolicySchema()
