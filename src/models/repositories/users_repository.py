from src.models.connection.db_connection_handler import DbConnectionHandler
from src.models.entities.users import Users
from .interfaces.users_repository import UsersRepositoryInterface

class UsersRepository(UsersRepositoryInterface):
    def __init__(self, db_conn_handler: DbConnectionHandler):
        self.__db_conn_handler = db_conn_handler
    
    def insert_user(self, name: str, email: int, password) -> None:
        with self.__db_conn_handler as database:
            try:
                new_user = Users(
                    name = name,
                    email = email,
                    password = password
                )
                database.session.add(new_user)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def select_user(self, email: str) -> Users:
        with self.__db_conn_handler as database:
            user = (
                database.session.query(Users)
                .filter(Users.email == email)
                .first()
            )
            return user
