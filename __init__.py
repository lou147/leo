from flask import Flask
from models import db, User, Tag, Article, Comment
from blog.views import blog_blueprint
from control.views import control_blueprint
from api.views import api_blueprint
from upload import upload_blueprint
from extensions import login_manager, csrf, flask_admin, cache, assets_env, main_css, main_js
from flask_admin.menu import MenuLink
from admin import ArticleView, UserView, TagView, CommentView, FileAdminView, LoginMenuLink, LogoutMenuLink
import os
from flask_cors import CORS


def create_app(object_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(object_name)

    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    assets_env.init_app(app)
    assets_env.register('main_js', main_js)
    assets_env.register('main_css', main_css)

    flask_admin.init_app(app)
    flask_admin.add_link(MenuLink(name='home', category='', url="/"))
    flask_admin.add_view(ArticleView(Article, db.session, endpoint='article'))
    flask_admin.add_view(UserView(User, db.session, endpoint='user'))
    flask_admin.add_view(TagView(Tag, db.session, endpoint='tag'))
    flask_admin.add_view(CommentView(Comment, db.session, endpoint='comment'))
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
    flask_admin.add_view(FileAdminView(path, '/static/', name='Static Files'))
    flask_admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
    flask_admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))

    app.register_blueprint(blog_blueprint)
    app.register_blueprint(control_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(upload_blueprint)
    return app
