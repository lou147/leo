from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from filters import add_one
import models
from __init__ import create_app
import config
from flask_assets import ManageAssets
from ext import assets_env

app = create_app(config.DevConfig)
app.DEBUG = True
manager = Manager(app)
migrate = Migrate(app, models.db)
app.jinja_env.filters['add_one'] = add_one

manager.add_command("server", Server(threaded=True))
manager.add_command('db', MigrateCommand)
manager.add_command('assets', ManageAssets(assets_env))


@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=models.db,      # db,create_all()
        User=models.User,
        Article=models.Article,
        Comment=models.Comment,
        Tag=models.Tag,
        Server=Server
    )

if __name__ == '__main__':
    manager.run()
