from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from extensions import bcrypt
from flask_login.mixins import AnonymousUserMixin

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_super_user = db.Column(db.Boolean, default=False, index=True)
    articles = db.relationship('Article', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<Model User `{}`>".format(self.username)

    @staticmethod
    def set_password(password):
        return bcrypt.generate_password_hash(password=password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def get_id(self):
        return self.id

articles_tags = db.Table(
    'articles_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    abstract = db.Column(db.Text())
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_top = db.Column(db.Boolean, default=False, index=True)
    create_time = db.Column(db.DateTime, default=datetime.now(), index=True)
    edit_time = db.Column(db.DateTime, default=datetime.now(), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    comments = db.relationship('Comment', backref='articles', lazy='dynamic')
    tags = db.relationship('Tag', secondary=articles_tags, backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, text, abstract, is_active, is_top, user_id):
        self.title = title
        self.text = text
        self.abstract = abstract
        self.is_active = is_active
        self.is_top = is_top

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'abstract': self.abstract,
            'is_active': self.is_active,
            'is_top': self.is_top,
            'create_time': self.create_time,
            'edit_time': self.edit_time,
            'user_id': self.user_id,
            'tags': self.tags
        }


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.now())
    edit_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Model Tag `{}`>".format(self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time
        }


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    people_ip = db.Column(db.String(255))
    text = db.Column(db.Text())
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), index=True)
    create_time = db.Column(db.DateTime, default=datetime.now(), index=True)
    parent_comment = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True, index=True)

    def __init__(self, name, text, article_id):
        self.name = name
        self.text = text
        self.article_id = article_id

    def __repr__(self):
        return '<Model Comment `{}`>'.format(self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'people_ip': self.people_ip,
            'text': self.text,
            'create_time': self.create_time,
            'parent_comment': self.parent_comment
        }


