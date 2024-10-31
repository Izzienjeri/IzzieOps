# routes/onboarding_document.py
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import OnboardingDocument
from extensions import db
import uuid

onboarding_document_bp = Blueprint('onboarding_document', __name__)
api = Api(onboarding_document_bp)

onboarding_document_parser = reqparse.RequestParser()
onboarding_document_parser.add_argument('employee_id', required=True, help='Employee ID cannot be blank')
onboarding_document_parser.add_argument('document_type', required=True, help='Document type cannot be blank')
onboarding_document_parser.add_argument('document_path', required=True, help='Document path cannot be blank')

class OnboardingDocumentResource(Resource):
    def get(self, document_id):
        document = OnboardingDocument.query.get(document_id)
        if document:
            return {
                'id': document.id,
                'employee_id': document.employee_id,
                'document_type': document.document_type,
                'document_path': document.document_path,
                'submitted_at': document.submitted_at
            }, 200
        return {'message': 'Document not found'}, 404

    def post(self):
        args = onboarding_document_parser.parse_args()
        new_document = OnboardingDocument(
            id=str(uuid.uuid4()),
            employee_id=args['employee_id'],
            document_type=args['document_type'],
            document_path=args['document_path']
        )
        db.session.add(new_document)
        db.session.commit()
        return {'message': 'Onboarding document created', 'id': new_document.id}, 201

api.add_resource(OnboardingDocumentResource, '/onboarding-documents', '/onboarding-documents/<string:document_id>')
