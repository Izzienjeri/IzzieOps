from flask import request
from flask_restful import Resource
from models import db, Employee, OnboardingDocument
from datetime import datetime

class EmployeeResource(Resource):
    def post(self):
        data = request.get_json()
        new_employee = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            position=data['position'],
            department=data['department']
        )
        db.session.add(new_employee)
        db.session.commit()
        return {'id': new_employee.id}, 201

    def get(self, employee_id):
        employee = Employee.query.get(employee_id)
        if employee is None:
            return {'message': 'Employee not found'}, 404
        return {
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'phone': employee.phone,
            'position': employee.position,
            'department': employee.department
        }

# Add more methods (PUT, DELETE) as needed

