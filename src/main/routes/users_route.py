from flask import Blueprint, request
from src.models.user_model import UserSchema, AuthSchema
from src.controllers.user_controller import UserCreator, UserAuthenticate
from src.models.repositories.users_repository import UsersRepository

def user_routes(db):
    user_routes_bp = Blueprint("user_routes", __name__)

    @user_routes_bp.route("/api/v1/register", methods=["POST"])
    def register_user():
        data = request.get_json()
        user = UserSchema(**data)
        users_repository = UsersRepository(db)
        user_controller = UserCreator(users_repository)
        return user_controller.insert_new_user(user.name, user.email, user.password)

    @user_routes_bp.route("/api/v1/auth", methods=["POST"])
    def authenticate_user():
        data = request.get_json()
        user = AuthSchema(**data)
        users_repository = UsersRepository(db)
        user_controller = UserAuthenticate(users_repository)
        return user_controller.authenticate_user(user.email, user.password)

    return user_routes_bp