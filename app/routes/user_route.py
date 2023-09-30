from flask import Blueprint
from app.controllers.user_controller import createUserController, loginUserController, getUserController
from app.utils.constants import API_VERSION
from flask_jwt_extended import jwt_required


user_route = Blueprint('user_route', __name__)

RESOURCE_NAME = "user"

@user_route.route(f'{API_VERSION}/{RESOURCE_NAME}/users', methods=['POST'])
def create_user():
    return createUserController()

@user_route.route(f'{API_VERSION}/{RESOURCE_NAME}/users', methods=['GET'])
@jwt_required()
def get_user():
    return getUserController()

@user_route.route(f'{API_VERSION}/{RESOURCE_NAME}/users/login', methods=['POST'])
def login_user():
    return loginUserController()
