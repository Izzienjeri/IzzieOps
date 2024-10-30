from flask import Blueprint
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from models import db, Employee, OnboardingDocument, WelcomeEmail, Policy

# Create a Blueprint for serializers
serializer_bp = Blueprint('serializer_bp', __name__)
ma = Marshmallow(serializer_bp)

# Employee Schema
class EmployeeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        include_fk = True  # Include foreign keys
        exclude = ('password',)  # Exclude password for security

    onboarding_documents = fields.Nested('OnboardingDocumentSchema', many=True)  # Nested relation

employee_schema = EmployeeSchema()  # Use snake_case for instance variables

# OnboardingDocument Schema
class OnboardingDocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OnboardingDocument
        include_fk = True  # Include foreign keys

    employee_id = fields.String(required=True)  # Optionally validate employee_id if needed

onboarding_document_schema = OnboardingDocumentSchema()

# WelcomeEmail Schema
class WelcomeEmailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WelcomeEmail
        include_fk = True  # Include foreign keys

    employee_id = fields.String(required=True)  # Optionally validate employee_id if needed

welcome_email_schema = WelcomeEmailSchema()

# Policy Schema
class PolicySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Policy
        include_fk = True  # Include foreign keys

policy_schema = PolicySchema()
