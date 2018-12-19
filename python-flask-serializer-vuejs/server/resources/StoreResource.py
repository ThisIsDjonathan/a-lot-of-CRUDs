from Serializer import AlchemyEncoder
import json
from flask_restful import Resource
from flask_restful import Resource, reqparse
from config import Store
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()

class GetStoreData(Resource):
    @jwt_required
    def get(self):
        parser.add_argument('id', type=str)
        storeId = parser.parse_args()
        return Store.query.filter_by(id=storeId).first()