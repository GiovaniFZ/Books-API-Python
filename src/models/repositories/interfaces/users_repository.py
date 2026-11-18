from abc import ABC, abstractclassmethod
from src.models.entities.users import Users

class UsersRepositoryInterface(ABC):
    @abstractclassmethod
    def insert_user(self, name: str, email: str, password: str) -> None:
        pass

    @abstractclassmethod
    def select_user(self, email: str) -> list[Users]:
        pass