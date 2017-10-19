from flask import Blueprint, request
from flask_restful import reqparse
from models import db, Comment, Article, Tag
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from flask_login import current_user
from sqlalchemy.sql import exists


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


api_blueprint = Blueprint('api', __name__, url_prefix='/api')


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
        data = eval(data)
        article_id = data.get('article_id')
        name = data.get('name')
        text = data.get('comment_content')
        comment_obj = Comment(name=name, text=text, article_id=article_id)
        db.session.add(comment_obj)
        db.session.commit()
        return ''
    else:
        return 'wrong request methods'


@api_blueprint.route('/article', methods=['GET', 'POST', 'PUT', 'DELETE'])
def article_api():
    if not current_user.is_super_user:
        return 'no permission'

    if request.method == 'GET':
        article_info = db.session.query(Article).all()
        article_list = list()
        for i in article_info:
            article_list.append(i.to_json())
        return json.dumps(article_list, cls=AlchemyEncoder)
    if request.method == 'POST':
        data = request.data
        if data:
            data = eval(data)
            title = data['title']
            content = data['content']
            is_active = data['is_active']
            is_top = data['is_top']
            user_id = data['user_id']
            tag_list = data['tag_list']
            article_obj = Article(title=title, text=content, abstract=content[:200], is_active=is_active,
                                  is_top=is_top, user_id=user_id)
            if tag_list:
                article_obj.tags = [Tag.query.filter_by(id=tag['id']).one() for tag in tag_list]
            db.session.add(article_obj)
            db.session.commit()
            return json.dumps({'article_id': article_obj.id})
        else:
            return 'no data'
    if request.method == 'PUT':
        data = request.data
        if data:
            data = eval(data)
            article_id = data['id']
            title = data['title']
            content = data['content']
            tag_list = data['tag_list']
            article_obj = Article.query.filter_by(id=article_id)
            article_obj.update({
                'title': title, 'text': content, 'abstract': content[:200]
            })
            if tag_list:
                article_obj.one().tags = [Tag.query.filter_by(id=i.get('id')).one() for i in tag_list]
            db.session.commit()
        return 'put success'
    if request.method == 'DELETE':
        data = request.data
        if data:
            data = eval(data)
            article_id = data['article_id']
            article_obj = Article.query.filter_by(id=article_id)
            db.session.delete(article_obj.one())
            db.session.commit()
        return 'put success'

    else:
        return 'wrong request methods'


@api_blueprint.route('/tag', methods=['GET', 'POST'])
def tag_api():
    if request.method == 'GET':
        parser = reqparse.RequestParser()
        parser.add_argument('article_id', type=int, help='Rate cannot be converted')
        args = parser.parse_args()
        article_id = args.get('article_id')
        if article_id:
            tag_info = Article.query.filter_by(id=article_id).one().tags
        else:
            tag_info = db.session.query(Tag).all()
        tag_list = list()
        for i in tag_info:
            tag_list.append(i.to_json())
        return json.dumps(tag_list, cls=AlchemyEncoder)
    if request.method == 'POST':
        data = request.data
        if data:
            data = eval(data)
            name = data.get('name').strip()
            if ' ' in name:
                return 'not include space'
            if db.session.query(exists().where(Tag.name == name)).scalar():
                return 'tag exists'
            if len(name) < 1:
                return 'wrong tag'
            else:
                tag_obj = Tag(name=name)
                db.session.add(tag_obj)
                db.session.commit()
                return 'success'
        else:
            return 'no data'
    else:
        return 'wrong request methods'
