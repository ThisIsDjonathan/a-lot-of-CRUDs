from Serializer import AlchemyEncoder
import json
from passlib.apps import custom_app_context as pwd_context
from flask_restful import Resource, reqparse
from config import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()

class GetUser(Resource):
    def get(self):
        users = User.query.all()
        users_json = []
        for user in users:
            users_json.append(json.dumps(user, cls=AlchemyEncoder))
        return {'status': 'success', 'data': users_json}, 200

class UserRegistration(Resource):
    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        data = parser.parse_args()

        already_exists = User.get_user_by_email(self, data['email'])
        if already_exists:
            return {'message': 'Usuário já existe'}, 400

        new_user = User()
        new_user.public_id = 100
        new_user.name = data['name']
        new_user.last_name = data['last_name']
        new_user.email = data['email']
        new_user.password = pwd_context.encrypt(data['password'])
        new_user.admin = False

        try:
            User.save(new_user)
            return { 'message': 'Usuário criado' }
        except Exception as e:
            print(str(e))
            return {'message': 'Ocorreu um erro'}, 500

class UserLogin(Resource):
    def post(self):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        data = parser.parse_args()
        current_user = User.get_user_by_email(self, data['email'])
        if not current_user:
            return {'message': 'Usuário não encontrado'}
        if self.verify_password(data['password'], current_user.password):
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(identity=data['email'])
            return {
                'message': 'Usuário logado com sucesso',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Senha inválida'}

    def verify_password(self, inputed_password, user_password):
        return pwd_context.verify(inputed_password, user_password)

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}