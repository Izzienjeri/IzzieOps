from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from extensions import db, mail  # Import mail here
from models import Employee, OnboardingDocument, WelcomeEmail, Policy, EmployeeProfile
from flask_mail import Message
import uuid

# Create Blueprint and API
onboarding_bp = Blueprint('onboarding', __name__)
api = Api(onboarding_bp)

register_parser = reqparse.RequestParser()
register_parser.add_argument('first_name', type=str, required=True, help="First name is required")
register_parser.add_argument('last_name', type=str, required=True, help="Last name is required")
register_parser.add_argument('email', type=str, required=True, help="Email is required")
register_parser.add_argument('phone', type=str, required=True, help="Phone number is required")
register_parser.add_argument('password', type=str, required=True, help="Password is required")

# Define Profile Update Parser
profile_parser = reqparse.RequestParser()
profile_parser.add_argument('position', type=str, required=False)
profile_parser.add_argument('department', type=str, required=False)
profile_parser.add_argument('bank_name', type=str, required=False)
profile_parser.add_argument('branch_name', type=str, required=False)
profile_parser.add_argument('account_name', type=str, required=False)
profile_parser.add_argument('account_number', type=str, required=False)

# Document Submission Parser
doc_parser = reqparse.RequestParser()
doc_parser.add_argument('employee_id', type=str, required=True, help="Employee ID is required")
doc_parser.add_argument('document_type', type=str, required=True, help="Document type is required")
doc_parser.add_argument('document_path', type=str, required=True, help="Document path is required")

# Bank Details Parser
bank_parser = reqparse.RequestParser()
bank_parser.add_argument('bank_name', type=str, required=True, help="Bank name is required")
bank_parser.add_argument('branch_name', type=str, required=False)
bank_parser.add_argument('account_name', type=str, required=True, help="Account name is required")
bank_parser.add_argument('account_number', type=str, required=True, help="Account number is required")

class RegisterEmployee(Resource):
    def post(self):
        args = register_parser.parse_args()
        employee = Employee(
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            phone=args['phone']
        )
        employee.set_password(args['password'])

        # Save employee
        db.session.add(employee)
        db.session.commit()

        # Send welcome email
        msg = Message(subject="Welcome to the Company", 
                      sender=mail.default_sender, 
                      recipients=[employee.email])
        msg.body = "Welcome to the team! Please complete your onboarding tasks."
        mail.send(msg)

        return jsonify({"message": "Employee registered successfully, welcome email sent."})

class UpdateEmployeeProfile(Resource):
    def put(self, employee_id):
        args = profile_parser.parse_args()
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"message": "Employee not found"}), 404

        # Check if the employee already has a profile
        if not employee.profile:
            profile = EmployeeProfile(employee_id=employee.id)
            db.session.add(profile)
        else:
            profile = employee.profile

        # Update profile fields if provided
        profile.position = args['position'] if args['position'] else profile.position
        profile.department = args['department'] if args['department'] else profile.department
        profile.bank_name = args['bank_name'] if args['bank_name'] else profile.bank_name
        profile.branch_name = args['branch_name'] if args['branch_name'] else profile.branch_name
        profile.account_name = args['account_name'] if args['account_name'] else profile.account_name
        profile.account_number = args['account_number'] if args['account_number'] else profile.account_number
        
        db.session.commit()
        return jsonify({"message": "Employee profile updated successfully"})

class SubmitDocument(Resource):
    def post(self):
        args = doc_parser.parse_args()
        document = OnboardingDocument(
            employee_id=args['employee_id'],
            document_type=args['document_type'],
            document_path=args['document_path']
        )
        db.session.add(document)
        db.session.commit()
        
        return jsonify({"message": "Document submitted successfully"})

class UpdateBankDetails(Resource):
    def put(self, employee_id):
        args = bank_parser.parse_args()
        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"message": "Employee not found"}), 404

        # Update bank details
        employee.bank_name = args['bank_name']
        employee.branch_name = args.get('branch_name', '')
        employee.account_name = args['account_name']
        employee.account_number = args['account_number']
        db.session.commit()

        return jsonify({"message": "Bank details updated successfully"})

class WelcomeEmailStatus(Resource):
    def get(self, employee_id):
        email = WelcomeEmail.query.filter_by(employee_id=employee_id).first()
        if not email:
            return jsonify({"message": "No welcome email record found"}), 404
        
        status = {"sent_at": email.sent_at, "opened": bool(email.opened_at)}
        return jsonify(status)

class GetPolicies(Resource):
    def get(self):
        policies = Policy.query.all()
        policy_list = [{"title": policy.title, "content": policy.content} for policy in policies]
        return jsonify({"policies": policy_list})

# Register routes
api.add_resource(RegisterEmployee, '/register')
api.add_resource(SubmitDocument, '/submit-document')
api.add_resource(UpdateBankDetails, '/<string:employee_id>/update-bank-details')
api.add_resource(WelcomeEmailStatus, '/<string:employee_id>/welcome-email-status')
api.add_resource(GetPolicies, '/policies')
api.add_resource(UpdateEmployeeProfile, '/<string:employee_id>/update-profile')

