from Serializer import AlchemyEncoder
import json
from flask_restful import Resource
from flask_restful import Resource, reqparse
from config import Factory
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()

class FactoryResource(Resource):
    def get(self):
        factories = Factory.query.all()
        factories_json = []

        for factory in factories:
            factories_json.append(json.dumps(factory, cls=AlchemyEncoder))

        return {'status': 'success', 'data': factories_json}, 200

class GetFactoryById(Resource):
    @jwt_required
    def get(self):
        parser.add_argument('id', type=str)
        data = parser.parse_args()
        return data