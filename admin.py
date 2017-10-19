from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink
from flask_login import current_user
from flask import redirect


class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect('/login')
        if current_user.is_authenticated and not current_user.is_super_user:
            return redirect('/login')
        return super(MyAdminIndexView, self).index()


class MyAdminModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_super_user


class ArticleView(MyAdminModelView):
    column_exclude_list = ['text', 'abstract']
    column_filters = ['text', 'title']


class UserView(MyAdminModelView):
    column_exclude_list = ['password', 'articles']
    column_filters = ['username']


class TagView(MyAdminModelView):
    column_filters = ['name']


class CommentView(MyAdminModelView):
    column_filters = ['name', 'text']


class FileAdminView(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_super_user


class LoginMenuLink(MenuLink):

    def is_accessible(self):
        return not current_user.is_authenticated


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated


