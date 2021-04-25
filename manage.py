import datetime
from getpass import getpass

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db
from app.auth.security import hash_password
from app.models.Project import Project, SubProject, ImageStore, ImageCategory, AllowedUser
from app.models.Excel import ExcelRecord, ExcelColumn
from app.models.Database import DatabaseCategory, Image, Database
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
    user = User.query.filter_by(is_admin=True).first()
    if user:
        print(f"Admin Account already exist. The username is '{user.email}'. To change password, run python manage.py "
              f"change_admin_password")
        exit()

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
        password=password,
        # password=hash_password(password),
        is_admin=True,
        is_active=True,
        first_name="Super",
        last_name="Admin",
        email_verified_at=datetime.datetime.now())
    user.create()
    print("Account was created successfully.")


@manager.command
def change_admin_password():
    """Changes Super admin password."""
    password = " "
    confirm_password = ""
    while password != confirm_password:
        password = getpass("New password: ")
        confirm_password = getpass("Confirm Password: ")
        if password and confirm_password and confirm_password != password:
            print("Password do not match")

    user = User.query.filter_by(is_admin=True).first()
    if user:
        user.password = password
        user.save()
        print("Password was updated successfully.")
    else:
        "No admin account found, please run python manage.py create_admin to modify_access an admin account"


if __name__ == '__main__':
    manager.run()
