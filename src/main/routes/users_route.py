from flask import Blueprint, request
from src.models.user_model import UserSchema
from src.controllers.user_creator import UserCreator
from src.models.repositories.users_repository import UsersRepository
from src.models.connection.db_connection_handler import DbConnectionHandler

user_routes_bp = Blueprint("user_routes", __name__)

@user_routes_bp.route("/api/v1/register", methods=["POST"])
def register_user():
    data = request.get_json()
    user = UserSchema(**data)
    db = DbConnectionHandler()
    users_repository = UsersRepository(db)
    user_controller = UserCreator(users_repository)
    user_controller.insert_new_user(user.name, user.email, user.password)
    return {"message": "User registered successfully"}, 201