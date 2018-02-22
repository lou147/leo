from controllers.api.views import api_blueprint
from controllers.blog.views import blog_blueprint
from flask import Flask
from flask_cors import CORS
from controllers.manage.views import control_blueprint
from filters import format_time, html_to_text, time_human
from models import db
from upload import upload_blueprint
from my_jwt import jwt_decoding
from flask_wtf import CSRFProtect
from ext import login_manager, cache, assets_env, main_css


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.get(user_id)


@login_manager.request_loader
def load_user_from_request(request):
    from models import User
    api_key = request.headers.get('token')
    print(api_key)
    if api_key:
        obj = jwt_decoding(api_key)
        print(obj)
        user = obj['some']
        if user:
            user = User.query.get(user['id'])
            return user
        else:
            print("is exception !!!!"+str(obj['error_msg']))
            return None


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    CORS(app)

    assets_env.init_app(app)
    assets_env.register('main_css', main_css)

    cache.init_app(app)

    csrf = CSRFProtect(app)
    csrf.exempt(api_blueprint)
    csrf.init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(control_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(upload_blueprint)

    app.add_template_filter(format_time, 'format_time')
    app.add_template_filter(html_to_text, 'html_to_text')
    app.add_template_filter(time_human, 'time_human')

    return app
