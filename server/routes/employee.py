# employee.py
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from models import Employee, db
from serializer import employee_schema

employee_bp = Blueprint('employee_bp', __name__)
api = Api(employee_bp)

# Request parser for creating an employee
employee_parser = reqparse.RequestParser()
employee_parser.add_argument('first_name', required=True, help='First name cannot be blank')
employee_parser.add_argument('last_name', required=True, help='Last name cannot be blank')
employee_parser.add_argument('email', required=True, help='Email cannot be blank')
employee_parser.add_argument('phone', required=False)
employee_parser.add_argument('position', required=True, help='Position cannot be blank')
employee_parser.add_argument('department', required=True, help='Department cannot be blank')
employee_parser.add_argument('password', required=True, help='Password cannot be blank')

class EmployeeResource(Resource):
    def post(self):
        args = employee_parser.parse_args()
        new_employee = Employee(
            first_name=args['first_name'],
            last_name=args['last_name'],
            email=args['email'],
            phone=args['phone'],
            position=args['position'],
            department=args['department']
        )
        new_employee.set_password(args['password'])
        db.session.add(new_employee)
        db.session.commit()
        return employee_schema.dump(new_employee), 201

    def get(self, employee_id):
        employee = Employee.query.get_or_404(employee_id)
        return employee_schema.dump(employee)

api.add_resource(EmployeeResource, '/employees', '/employees/<string:employee_id>')
