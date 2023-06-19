from flask import Flask
import os 
from init import db, ma, bcrypt, jwt
# import Blueprints
from controllers.cli_controller import db_commands

# application factory - when flask run, by default, the create_app function will be run first
def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # initialize libraries and connect them with the app 
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)

    return app