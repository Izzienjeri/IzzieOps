# policy.py
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from models import Policy, db
from serializer import policy_schema

policy_bp = Blueprint('policy_bp', __name__)
api = Api(policy_bp)

# Request parser for policies
policy_parser = reqparse.RequestParser()
policy_parser.add_argument('title', required=True, help='Title cannot be blank')
policy_parser.add_argument('content', required=True, help='Content cannot be blank')

class PolicyResource(Resource):
    def post(self):
        args = policy_parser.parse_args()
        new_policy = Policy(
            title=args['title'],
            content=args['content']
        )
        db.session.add(new_policy)
        db.session.commit()
        return policy_schema.dump(new_policy), 201

    def get(self):
        policies = Policy.query.all()
        return policy_schema.dump(policies, many=True)

api.add_resource(PolicyResource, '/policies')
