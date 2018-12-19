from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api
from config import app

import resources.FactoryResource as FactoryResource
import resources.UserResource as UserResource

# Setup
blueprint = Blueprint('api', __name__)
api = Api(blueprint, prefix="/api")

# Routes
api.add_resource(FactoryResource.FactoryResource, "/factory")
api.add_resource(FactoryResource.GetFactoryById, "/factory/get")
api.add_resource(UserResource.UserRegistration, '/user/registration')
api.add_resource(UserResource.UserLogin, '/user/login')


# Start app
app.register_blueprint(blueprint)
app.run()



