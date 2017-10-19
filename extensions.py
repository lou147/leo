from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_cache import Cache
from admin import MyAdminIndexView
from flask_assets import Environment, Bundle


assets_env = Environment()

main_css = Bundle(
    'css/blog.css',
    'css/grids-responsive-min.css',
    'css/pure-min.css',

    filters='cssmin',
    output='assets/css/common.css')

main_js = Bundle(
    'js/axios.min.js',
    'js/jquery-3.1.0.min.js',
    'js/vue.js',
    filters='jsmin',
    output='assets/js/common.js')

bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
cache = Cache()
flask_admin = Admin(index_view=MyAdminIndexView(name='Main', template='admin_template/index.html', url='/admin'),
                    endpoint='MyAdmin', name='Admin')


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.filter_by(id=user_id).first()
