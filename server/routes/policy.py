# routes/policy.py
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import Policy
from extensions import db
import uuid

policy_bp = Blueprint('policy', __name__)
api = Api(policy_bp)

policy_parser = reqparse.RequestParser()
policy_parser.add_argument('title', required=True, help='Title cannot be blank')
policy_parser.add_argument('content', required=True, help='Content cannot be blank')

class PolicyResource(Resource):
    def get(self, policy_id):
        policy = Policy.query.get(policy_id)
        if policy:
            return {
                'id': policy.id,
                'title': policy.title,
                'content': policy.content,
                'created_at': policy.created_at,
                'updated_at': policy.updated_at
            }, 200
        return {'message': 'Policy not found'}, 404

    def post(self):
        args = policy_parser.parse_args()
        new_policy = Policy(
            id=str(uuid.uuid4()),
            title=args['title'],
            content=args['content']
        )
        db.session.add(new_policy)
        db.session.commit()
        return {'message': 'Policy created', 'id': new_policy.id}, 201

api.add_resource(PolicyResource, '/policies', '/policies/<string:policy_id>')
