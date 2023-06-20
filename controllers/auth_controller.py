from flask import Blueprint, request
from init import db, bcrypt, jwt  
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/signup", methods=["POST"])
def auth_register():
    try:
        # pass data to the body of the request, which is done in Insomnia (front end)
        # extract the data in json structure to body {"name" : "User3", "email": "user2@email.com", "password": "user3pw"}
        body_data = request.get_json()

        # create a new User model instance from the user info
        # get the data from front end to the User model 
        user = User() # user is an instance of User class, which is the SQLAlchemy model
        user.name = body_data.get("name")
        user.email = body_data.get("email")
        # handling null password error
        if body_data.get("password"):
            user.password = bcrypt.generate_password_hash(body_data.get("password")).decode("utf-8")
        # add the user to the session
        db.session.add(user)
        # commit to add the user to the database
        db.session.commit()
        # respond to the client (pass the data back to front end)
        return user_schema.dump(user), 201

    # handling error for IntegrityError such as "email already registered" or "email is required"
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error" : "Email address already exists"}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error" : f'The {err.orig.diag.column_name} can not be blank'}, 409
    









