# employee.py
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import Employee
from extensions import db
import uuid

employee_bp = Blueprint('employee', __name__)
api = Api(employee_bp)

# Define request parsers for various routes
employee_parser = reqparse.RequestParser()
employee_parser.add_argument('first_name', required=True, help='First name cannot be blank')
employee_parser.add_argument('last_name', required=True, help='Last name cannot be blank')
employee_parser.add_argument('email', required=True, help='Email cannot be blank')
employee_parser.add_argument('phone')
employee_parser.add_argument('position', required=True, help='Position cannot be blank')
employee_parser.add_argument('department', required=True, help='Department cannot be blank')
employee_parser.add_argument('password', required=True, help='Password cannot be blank')

class EmployeeResource(Resource):
    def get(self, employee_id):
        employee = Employee.query.get(employee_id)
        if employee:
            return {
                'id': employee.id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'email': employee.email,
                'phone': employee.phone,
                'position': employee.position,
                'department': employee.department
            }, 200
        return {'message': 'Employee not found'}, 404

    def post(self):
        args = employee_parser.parse_args()
        new_employee = Employee(
            id=str(uuid.uuid4()),
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            phone=args['phone'],
            position=args['position'],
            department=args['department']
        )
        new_employee.set_password(args['password'])  # Make sure to hash the password
        db.session.add(new_employee)
        db.session.commit()
        return {'message': 'Employee created', 'id': new_employee.id}, 201

api.add_resource(EmployeeResource, '/employees', '/employees/<string:employee_id>')
