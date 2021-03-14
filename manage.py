from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.models import Project, Category, Image

app = create_app('development')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, project=project, category=category, image=image)


if __name__ == '__main__':
    manager.run()
