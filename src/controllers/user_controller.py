from src.models.repositories.interfaces.users_repository import UsersRepositoryInterface
from src.view.user_view import UserView
from src.controllers.errors.user_already_exists_error import UserAlreadyExistsError
from src.controllers.errors.user_not_found_error import UserNotFoundError
from src.controllers.errors.invalid_password_error import InvalidPasswordError
from src.models.entities.users import Users
from dotenv import load_dotenv
import os, jwt, bcrypt

class UserCreator:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self.__users_repo = users_repository
        load_dotenv()

    def insert_new_user(self, name: str, email: str, password: str) -> dict:
        try:
            self.__check_if_user_exists(email)
            self.__create_new_user(name, email, password)
            return UserView.show_message("User created successfully", 201, True)
        except UserAlreadyExistsError as error:
            if isinstance(error, UserAlreadyExistsError):
                return UserView.show_message(error.message, error.status)
            return UserView.show_message("Internal server error", 500)

    def __check_if_user_exists(self, email: str) -> None:
        select_user = self.__users_repo.select_user(email)
        if (not select_user):
            return
        raise UserAlreadyExistsError()

    def __create_new_user(self, name: str, email: str, password: str) -> None:
        password_hash = self.__hash_password(password)
        self.__users_repo.insert_user(name, email, password_hash)
        
    def __hash_password(self, password: str) -> str:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed
        
        
class UserAuthenticate:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self.__users_repo = users_repository
        
    def authenticate_user(self, email: str, input_password: str) -> dict:
        try:
            user = self.__check_if_user_exists(email)
            self.__check_password(input_password, user)
            token = self.__generate_jwt_token(user)
            return UserView.show_message(token, 200)
        except Exception as error:
            if (isinstance(error, (UserNotFoundError, InvalidPasswordError))):
                return UserView.show_message(error.message, error.status)
            print(error)
            return UserView.show_message("Internal server error", 500)
            
    def __check_if_user_exists(self, email) -> None:
        select_user = self.__users_repo.select_user(email)
        if (select_user):
            return select_user
        raise UserNotFoundError()
    
    def __check_password(self, input_password: str, user: Users) -> None:
        user_password = user.password.encode('utf-8')
        is_password_correct = bcrypt.checkpw(input_password.encode('utf-8'), user_password)
        if (is_password_correct):
            return
        raise InvalidPasswordError()
    
    def __generate_jwt_token(self, user: Users) -> dict:
        payload = {
            "sub": str(user.id),
            "email": user.email
        }
        secret = os.getenv("JWT_SECRET")
        token = jwt.encode(payload, secret, algorithm="HS256")
        return token
