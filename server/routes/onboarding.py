from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from extensions import db, mail
from models import Employee, OnboardingDocument, Policy, EmployeeProfile
from flask_mail import Message
from werkzeug.security import generate_password_hash
from datetime import datetime

onboarding_bp = Blueprint('onboarding', __name__)
api = Api(onboarding_bp)

# Registration Parser
register_parser = reqparse.RequestParser()
register_parser.add_argument('first_name', type=str, required=True, help="First name is required")
register_parser.add_argument('last_name', type=str, required=True, help="Last name is required")
register_parser.add_argument('email', type=str, required=True, help="Email is required")
register_parser.add_argument('phone', type=str, required=True, help="Phone number is required")
register_parser.add_argument('password', type=str, required=True, help="Password is required")

# Profile Update Parser
profile_parser = reqparse.RequestParser()
profile_parser.add_argument('position', type=str, required=True)
profile_parser.add_argument('department', type=str, required=True)
profile_parser.add_argument('national_id_number', type=str, required=True, help="National ID number is required")
profile_parser.add_argument('kra_pin_number', type=str, required=True, help="KRA PIN number is required")
profile_parser.add_argument('bank_name', type=str, required=True, help="Bank name is required")
profile_parser.add_argument('branch_name', type=str, required=True)
profile_parser.add_argument('account_name', type=str, required=True, help="Account name is required")
profile_parser.add_argument('account_number', type=str, required=True, help="Account number is required")

# Document Submission Parser
doc_parser = reqparse.RequestParser()
doc_parser.add_argument('document_type', type=str, required=True, choices=('National ID', 'KRA Certificate'), help="Document type must be either 'National ID' or 'KRA Certificate'")
doc_parser.add_argument('document_path', type=str, required=True, help="Document path is required")


class RegisterEmployee(Resource):
    def post(self):
        args = register_parser.parse_args()
        password_hash = generate_password_hash(args['password'])
        employee = Employee(
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            phone=args['phone'],
            password=password_hash
        )

        # Save employee
        db.session.add(employee)
        db.session.commit()

        # Send welcome email
        subject = "Welcome to IzzieOps"  # Define the subject here
        body = "Welcome! Here are some important details for you.."
        msg = Message(subject=subject, 
                      sender=mail.default_sender,
                      recipients=[args['email']],
                      body="Welcome, {}! Your account has been created.".format(args['first_name']))
        mail.send(msg)

        return {"message": "Employee registered successfully!"}, 201
    
class UpdateEmployeeProfile(Resource):
    def put(self, employee_id):
        args = profile_parser.parse_args()
        employee = Employee.query.get(employee_id)
        if not employee:
            return {"message": "Employee not found"}, 404

        if not employee.profile:
            profile = EmployeeProfile(employee_id=employee.id,
                                      national_id_number=args['national_id_number'],
                                      kra_pin_number=args['kra_pin_number'])
            db.session.add(profile)
        else:
            profile = employee.profile
            profile.national_id_number = args['national_id_number']
            profile.kra_pin_number = args['kra_pin_number']

        profile.position = args.get('position', profile.position)
        profile.department = args.get('department', profile.department)
        profile.bank_name = args.get('bank_name', profile.bank_name)
        profile.branch_name = args.get('branch_name', profile.branch_name)
        profile.account_name = args.get('account_name', profile.account_name)
        profile.account_number = args.get('account_number', profile.account_number)
        
        db.session.commit()
        return {"message": "Employee profile updated successfully"}, 200

class SubmitDocument(Resource):
    def post(self, employee_id):
        args = doc_parser.parse_args()

        document = OnboardingDocument(
            employee_id=employee_id,  # Use employee_id from the URL
            document_type=args['document_type'],
            document_path=args['document_path']
        )
        db.session.add(document)
        db.session.commit()
        
        return {"message": "Document submitted successfully"}, 201


class GetPolicies(Resource):
    def get(self):
        policies = Policy.query.all()
        policy_list = [{"title": policy.title, "content": policy.content} for policy in policies]
        return {"policies": policy_list}

api.add_resource(RegisterEmployee, '/register')
api.add_resource(UpdateEmployeeProfile, '/<string:employee_id>/update-profile')
api.add_resource(SubmitDocument, '/<string:employee_id>/submit-document')  # Updated route
api.add_resource(GetPolicies, '/policies')
