from flask import Blueprint
from init import db, bcrypt
from models.user import User

# use blueprint to efficiently organise the routes/controllers
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Table dropped")

@db_commands.cli.command("seed")
def seed_db():
    users = [
        User(
            email = "admin@admin.com",
            password = bcrypt.generate_password_hash("admin123").decode("utf-8"),
            is_admin=True
        ),

        User(
            name = "User1",
            email = "user1@email.com",
            password = bcrypt.generate_password_hash("user1pw").decode("utf-8"),
        ),
        
        User(
            name = "User2",
            email = "user2@email.com",
            password = bcrypt.generate_password_hash("user2pw").decode("utf-8")
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    print("Table seeded")
