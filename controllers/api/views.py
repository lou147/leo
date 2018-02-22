from flask import Blueprint, request
from flask_restful import reqparse
from models import db, Comment, Article, Tag, User
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from my_jwt import jwt_encoding
from flask_login import login_required

api_blueprint = Blueprint('api', __name__, url_prefix='/api')


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj.__class__, DeclarativeMeta):
            data = obj.to_json()
            for i in data:
                if isinstance(i, DeclarativeMeta):
                    data[i] = data[i].to_json()
            return data
        return json.JSONEncoder.default(self, obj)


def instead_none(ori, val):
    if not ori:
        return val
    return ori


class PaginationObj(object):
    def __init__(self, page, d_num, db_model):
        if not page:
            page = 1
        self.d_num = d_num
        self.start = (page-1)*d_num
        self.page = page
        self.db_model = db_model

    def get_page_data(self):
        data_info = self.db_model.db.session.query(Article).join(User, isouter=True).order_by(Article.id.desc()).offset(self.start).limit(self.d_num).all()
        return data_info

    def get_page_nums(self):
        pass

def permit():
    # if not current_user.is_authenticated:
    #     return 'need login'
    # if not current_user.is_super_user:
    #     return 'need super user'
    pass


def get_or_create(mod, **kwargs):
    instance = mod.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        new_ins = mod(**kwargs)
        db.session.add(new_ins)
        db.session.commit()
        return new_ins


@api_blueprint.route('/article_list', methods=['GET'])
@login_required
def article_list_api():
    if request.method == 'GET':
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int)
        parser.add_argument('order_by', type=str)
        parser.add_argument('reverse', type=str)
        args = parser.parse_args()
        page = instead_none(args.get('page'), 1)
        order_by = instead_none(args.get('order_by'), 'create_time')
        reverse = instead_none(args.get('reverse'), 'desc')

        order_by_query = 'Article.{}.{}()'.format(order_by, reverse)
        article_page = Article.query.join(User, isouter=True).order_by(eval(order_by_query)).paginate(int(page), 10)
        article_info = article_page.items
        page_info = list(article_page.iter_pages())
        data = {
            'article_info': article_info,
            'page_info': page_info
        }
        return json.dumps(data, cls=AlchemyEncoder)


@api_blueprint.route('/article', methods=['GET', 'POST', 'PUT', 'DELETE'])
@api_blueprint.route('/article/<article_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def article_api(article_id=None):
    if request.method == 'GET':
        article_info = Article.query.get_or_404(article_id)
        return json.dumps(article_info, cls=AlchemyEncoder)

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return 'wrong post, empty data'
        text = data['text']
        tag_list = data['tags']
        tags = [get_or_create(Tag, name=tag) for tag in tag_list]
        article_obj = Article(title=data['title'], text=text, abstract=text[:200], is_active=data['is_active'],
                              is_top=data['is_top'], user_id=2)
        article_obj.tags = tags
        if data.get('create_time'):
            article_obj.create_time = data['create_time']
        if data.get('update_time'):
            article_obj.update_time = data['update_time']

        db.session.add(article_obj)
        db.session.commit()
        return json.dumps({'article_id': article_obj.id})

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return 'wrong post, empty data'
        article_info = Article.query.get_or_404(article_id)
        article_info.title = data['title']
        article_info.text = data['text']
        article_info.abstract = data['text'][:200]
        article_info.is_active = data['is_active']
        article_info.is_top = data['is_top']
        article_info.create_time = data['create_time']
        article_info.update_time = data['update_time']
        article_info.tags = [get_or_create(Tag, name=tag) for tag in data['tags']]
        db.session.commit()
        return 'put success'
    if request.method == 'DELETE':
        print('get start........')
        article_obj = Article.query.get(article_id)
        print('article obj....', article_obj)
        db.session.delete(article_obj)
        db.session.commit()
        return 'delete success'
    else:
        return 'wrong request methods'


@api_blueprint.route('/comment', methods=['GET', 'POST'])
def comment_api():
    if request.method == 'GET':
        parser = reqparse.RequestParser()
        parser.add_argument('article_id', type=int, help='Rate cannot be converted')
        args = parser.parse_args()
        article_id = args.get('article_id')
        comment_info = db.session.query(Comment).filter_by(article_id=article_id).all()
        comment_list = list()
        for i in comment_info:
            comment_list.append(i.to_json())
        return json.dumps(comment_list, cls=AlchemyEncoder)
    if request.method == 'POST':
        data = request.data
        if data:
            data = eval(data)
            article_id = data.get('article_id')
            name = data.get('name')
            text = data.get('comment_content')
            comment_obj = Comment(name=name, text=text, article_id=article_id)
            db.session.add(comment_obj)
            db.session.commit()
            return 'commit success'
        else:
            return 'no data'
    else:
        return 'wrong request methods'


@api_blueprint.route('/tag_list', methods=['GET'])
def tag_list_api():
    if request.method == 'GET':
        tag_list = Tag.query.all()
        return json.dumps(tag_list, cls=AlchemyEncoder)


@api_blueprint.route('/user_list', methods=['GET', 'POST'])
def user_list_api():
    if request.method == 'GET':
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int)
        parser.add_argument('order_by', type=str)
        parser.add_argument('reverse', type=str)
        args = parser.parse_args()
        page = instead_none(args.get('page'), 1)
        order_by = instead_none(args.get('order_by'), 'create_time')
        reverse = instead_none(args.get('reverse'), 'desc')

        order_by_query = 'User.{}.{}()'.format(order_by, reverse)
        user_page = User.query.order_by(eval(order_by_query)).paginate(int(page), 10)
        user_info = user_page.items
        page_info = list(user_page.iter_pages())
        data = {
            'user_info': user_info,
            'page_info': page_info
        }
        return json.dumps(data, cls=AlchemyEncoder)


@api_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    user_name = data['username']
    password = data['password']
    print(user_name)
    now_user = User.query.filter_by(username=user_name).first()
    print(now_user)
    if not now_user:
        return json.dumps({'status': 'fail', 'msg': 'not user'})
    if not now_user.check_password(password):
        return json.dumps({'status': 'fail', 'msg': 'wrong password'})

    user_info = {
        'id': now_user.id,
        'username': now_user.username
    }
    token = jwt_encoding(user_info).decode()
    user_info['token'] = token
    return json.dumps({'status': 'ok', 'user_info': user_info, 'msg': 'success'})
