from flask import request
from flask_restful import Resource
from models import db, OnboardingDocument
import datetime

class OnboardingDocumentResource(Resource):
    def post(self, employee_id):
        data = request.get_json()
        new_document = OnboardingDocument(
            employee_id=employee_id,
            document_type=data['document_type'],
            document_path=data['document_path'],
            submitted_at=datetime.utcnow()
        )
        db.session.add(new_document)
        db.session.commit()
        return {'id': new_document.id}, 201

    def get(self, employee_id):
        documents = OnboardingDocument.query.filter_by(employee_id=employee_id).all()
        return [{'id': doc.id, 'document_type': doc.document_type, 'document_path': doc.document_path} for doc in documents]

