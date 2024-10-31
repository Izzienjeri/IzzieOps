# onboarding_document.py
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from models import OnboardingDocument, db
from serializer import onboarding_document_schema

onboarding_document_bp = Blueprint('onboarding_document_bp', __name__)
api = Api(onboarding_document_bp)

# Request parser for onboarding documents
document_parser = reqparse.RequestParser()
document_parser.add_argument('employee_id', required=True, help='Employee ID cannot be blank')
document_parser.add_argument('document_type', required=True, help='Document type cannot be blank')
document_parser.add_argument('document_path', required=True, help='Document path cannot be blank')

class OnboardingDocumentResource(Resource):
    def post(self):
        args = document_parser.parse_args()
        new_document = OnboardingDocument(
            employee_id=args['employee_id'],
            document_type=args['document_type'],
            document_path=args['document_path']
        )
        db.session.add(new_document)
        db.session.commit()
        return onboarding_document_schema.dump(new_document), 201

    def get(self, employee_id):
        documents = OnboardingDocument.query.filter_by(employee_id=employee_id).all()
        return onboarding_document_schema.dump(documents, many=True)

api.add_resource(OnboardingDocumentResource, '/onboarding-documents', '/onboarding-documents/<string:employee_id>')
