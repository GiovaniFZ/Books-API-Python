from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.connection.base import Base
from src.models.entities.users import Users

class DbConnectionHandler:
    def __init__(self):
        self.__connection_string = "sqlite:///schema.db"
        self.__engine = self.__create_database_engine()
        self.session = None

    def create_tables(self):
        Base.metadata.create_all(bind=self.__engine)

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def __enter__(self):
        session_make = sessionmaker(bind = self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
