import os
import click
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


# export FLASK_APP=flasky.py
# `flask shell` ==> db, User, Role 등 명령어 할 수 있음
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# python flasky.py shell/db
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
