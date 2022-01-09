import os
import click
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@app.cli.command()
@manager.command
@click.argument('test_names', nargs=-1)
def test(test_names=None):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
