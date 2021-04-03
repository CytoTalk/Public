import datetime
from getpass import getpass

from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.auth.security import hash_password
from app.models import Excel
from app.models.User import User


app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def create_admin():
    """Creates the admin user."""
    email = input("Email Address: ")
    password = " "
    confirm_password = ""
    while password != confirm_password:
        password = getpass("Password: ")
        confirm_password = getpass("Confirm Password: ")
        if password and confirm_password and confirm_password != password:
            print("Password do not match")

    user = User(
        email=email,
        password=hash_password(password),
        is_admin=True,
        first_name="Super",
        last_name="Admin",
        email_verified_at=datetime.datetime.now())
    user.create()
    print("Account was created successfully.")


if __name__ == '__main__':
    manager.run()
