from flask_assets import Environment, Bundle
from flask_cache import Cache
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
login_manager = LoginManager()
cache = Cache()
assets_env = Environment()
main_css = Bundle(
        'css/blog.css',
        filters='cssmin',
        output='assets/css/common.css'
    )
