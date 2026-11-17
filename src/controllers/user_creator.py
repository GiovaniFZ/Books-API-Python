from src.models.repositories.interfaces.users_repository import UsersRepositoryInterface

class UserCreator:
    def __init__(self, users_repository: UsersRepositoryInterface):
        self.__users_repo = users_repository

    def insert_new_user(self, name: str, email: str, password: str) -> dict:
        self.__check_if_user_exists(name)
        self.__create_new_user(name, email, password)
        return self.__format_response()

    def __check_if_user_exists(self, name: str) -> None:
        select_users = self.__users_repo.select_user(name)
        if (not select_users or len(select_users) == 0):
            return
        raise Exception()

    def __create_new_user(self, name: str, email: str, password: str) -> None:
        self.__users_repo.insert_user(name, email, password)

    def __format_response(self) -> dict:
        return {"message": "Usuário cadastrado com sucesso"}
