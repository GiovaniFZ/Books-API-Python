from src.models.repositories.interfaces.users_repository import UsersRepositoryInterface
from src.view.user_creator_view import UserCreatorView
from src.controllers.errors.user_already_exists_error import UserAlreadyExistsError

class UserCreator:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self.__users_repo = users_repository

    def insert_new_user(self, name: str, email: str, password: str) -> dict:
        try:
            self.__check_if_user_exists(name)
            self.__create_new_user(name, email, password)
            return UserCreatorView.show_success_message()
        except UserAlreadyExistsError as error:
            return UserCreatorView.show_error_message(error.message), error.status

    def __check_if_user_exists(self, name: str) -> None:
        select_users = self.__users_repo.select_user(name)
        if (not select_users or len(select_users) == 0):
            return
        raise UserAlreadyExistsError()

    def __create_new_user(self, name: str, email: str, password: str) -> None:
        self.__users_repo.insert_user(name, email, password)
