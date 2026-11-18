from flask import Flask
from src.main.routes.users_route import user_routes
from src.models.connection.db_connection_handler import DbConnectionHandler

app = Flask(__name__)
db = DbConnectionHandler()
db.create_tables()
app.register_blueprint(user_routes(db))
