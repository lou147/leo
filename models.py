from ext import bcrypt
from datetime import datetime
from flask_login.mixins import AnonymousUserMixin
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Column = db.Column
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime
Integer = db.Integer
relationship = db.relationship
ForeignKey = db.ForeignKey
Text = db.Text


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    nick_name = Column(String(255), unique=True)
    avatar_path = Column(String(255), nullable=True)
    create_time = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True, index=True)
    is_super_user = Column(Boolean, default=False, index=True)
    articles = relationship('Article', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'nick_name': self.nick_name,
            'avatar_path': self.avatar_path,
            'create_time': self.create_time,
            'is_active': self.is_active,
            'is_super_user': self.is_super_user
        }

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
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Article(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    text = Column(Text())
    abstract = Column(Text())
    is_active = Column(Boolean, default=True, index=True)
    is_top = Column(Boolean, default=False, index=True)
    create_time = Column(DateTime, default=datetime.now(), index=True)
    update_time = Column(DateTime, default=datetime.now(), index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    comments = relationship('Comment', backref='articles', lazy='dynamic')
    tags = relationship('Tag', secondary=articles_tags, backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, text, abstract, is_active, is_top, user_id):
        self.title = title
        self.text = text
        self.abstract = abstract
        self.is_active = is_active
        self.is_top = is_top

    def count_star(self):
        count_query = (self.statement.with_only_columns([func.count()])
                       .order_by(None))
        return self.session.execute(count_query).scalar()

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
            'update_time': self.update_time,
            'user_id': self.user_id,
            'tags': self.tags
        }


class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    create_time = Column(DateTime, default=datetime.now())
    edit_time = Column(DateTime, onupdate=datetime.now())

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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    people_ip = Column(String(255))
    text = Column(Text())
    article_id = Column(Integer, ForeignKey('articles.id'), index=True)
    create_time = Column(DateTime, default=datetime.now(), index=True)
    parent_comment = Column(db.Integer, ForeignKey('comments.id'), nullable=True, index=True)

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


