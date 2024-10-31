# welcome_email.py
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from flask_mail import Mail, Message
from models import WelcomeEmail, db
from serializer import welcome_email_schema

welcome_email_bp = Blueprint('welcome_email_bp', __name__)
api = Api(welcome_email_bp)
mail = Mail()

# Request parser for welcome emails
email_parser = reqparse.RequestParser()
email_parser.add_argument('employee_id', required=True, help='Employee ID cannot be blank')
email_parser.add_argument('subject', required=True, help='Email subject cannot be blank')
email_parser.add_argument('body', required=True, help='Email body cannot be blank')

class WelcomeEmailResource(Resource):
    def post(self):
        args = email_parser.parse_args()
        new_email = WelcomeEmail(
            employee_id=args['employee_id'],
            subject=args['subject'],
            body=args['body']
        )
        db.session.add(new_email)
        db.session.commit()

        # Send welcome email
        msg = Message(subject=args['subject'], recipients=[args['employee_id']], body=args['body'])
        mail.send(msg)

        return welcome_email_schema.dump(new_email), 201

api.add_resource(WelcomeEmailResource, '/welcome-emails')
