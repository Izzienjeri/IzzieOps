# routes/welcome_email.py
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import WelcomeEmail
from extensions import db
import uuid

welcome_email_bp = Blueprint('welcome_email', __name__)
api = Api(welcome_email_bp)

welcome_email_parser = reqparse.RequestParser()
welcome_email_parser.add_argument('employee_id', required=True, help='Employee ID cannot be blank')
welcome_email_parser.add_argument('subject', required=True, help='Subject cannot be blank')
welcome_email_parser.add_argument('body', required=True, help='Body cannot be blank')

class WelcomeEmailResource(Resource):
    def get(self, email_id):
        email = WelcomeEmail.query.get(email_id)
        if email:
            return {
                'id': email.id,
                'employee_id': email.employee_id,
                'subject': email.subject,
                'body': email.body,
                'sent_at': email.sent_at
            }, 200
        return {'message': 'Welcome email not found'}, 404

    def post(self):
        args = welcome_email_parser.parse_args()
        new_email = WelcomeEmail(
            id=str(uuid.uuid4()),
            employee_id=args['employee_id'],
            subject=args['subject'],
            body=args['body']
        )
        db.session.add(new_email)
        db.session.commit()
        return {'message': 'Welcome email created', 'id': new_email.id}, 201

api.add_resource(WelcomeEmailResource, '/welcome-emails', '/welcome-emails/<string:email_id>')
