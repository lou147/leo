from flask import render_template, Blueprint
from sqlalchemy import func, or_
from models import db, User, Article, Tag, Comment, articles_tags
from flask_restful import reqparse
import os
from extensions import cache


blog_blueprint = Blueprint('blog', __name__, template_folder=os.path.join('templates/blog_template'), url_prefix='')


@blog_blueprint.route('/')
@blog_blueprint.route('/page/<page>')
def home(page=1):
    if not page:
        page = 1
    articles = Article.query.order_by(Article.id.desc()).paginate(int(page), 10)
    return render_template('blog_template/home.html', article_list=articles)


@blog_blueprint.route('/post/<article_id>', methods=['GET', 'POST'])
def article_detail(article_id):
    if article_id.isdigit():
        article_info = Article.query.get(article_id)
        pre_article_info = Article.query.order_by(Article.id.asc()).filter(Article.id > article_info.id).first()
        next_article_info = Article.query.order_by(Article.id.desc()).filter(Article.id < article_info.id).first()
        tag_list = article_info.tags

        comments = article_info.comments.order_by(Comment.create_time.desc()).all()
        return render_template('blog_template/detail.html', article_info=article_info, tag_list=tag_list,
                               pre_article=pre_article_info, next_article=next_article_info, comments=comments)
    else:
        return '404'


@blog_blueprint.route('/tags')
@blog_blueprint.route('/tags/<tag_name>')
@blog_blueprint.route('/tags/<tag_name>/<page>')
def tags(tag_name=None, page=1):
    tag_list = Tag.query.all()
    if tag_name:
        if not page:
            page = 1
        tag = Tag.query.filter_by(name=tag_name).first_or_404()
        article_list = tag.articles.order_by(Article.create_time.desc()).paginate(int(page), 10)
        return render_template(template_name_or_list='blog_template/tags.html', tag_list=tag_list,
                               article_list=article_list, cur_tag=tag_name)
    else:
        article_list = []
        return render_template(template_name_or_list='blog_template/tags.html', tag_list=tag_list,
                               article_list=article_list, cur_tag=None)


@blog_blueprint.route('/archives')
def archives():
    article_list = db.session.query(Article.id, Article.title, Article.create_time).order_by(Article.create_time.desc()).all()
    print(article_list)
    archives_list = list()
    article_month_dict = dict()
    for article in article_list:
        article_month = str(article.create_time)[:7]
        if article_month_dict.get(article_month):
            article_month_dict[article_month].append(article)
        else:
            article_month_dict[article_month] = [article]
    for i in list(article_month_dict):
        archives_list.append({'month': i, 'article_list': article_month_dict[i]})
    return render_template('blog_template/archives.html', archives_list=archives_list)


@blog_blueprint.route('/about')
def about():

    return render_template('blog_template/about.html')


@blog_blueprint.route('/search', methods=['GET'])
def search():
    parser = reqparse.RequestParser()
    parser.add_argument('text', type=str)
    args = parser.parse_args().get('text')
    if args:
        article_list = Article.query.filter(
            or_(Article.title.contains(args), Article.text.contains(args))
        ).order_by(Article.create_time.desc()).all()
        tag_list = db.session.query(Tag.id, Tag.name).filter(Tag.name.contains(args))
        return render_template('blog_template/search.html', tag_list=tag_list, article_list=article_list)
    else:
        return '404'


@blog_blueprint.route('/edit', methods=['GET', 'POST'])
@blog_blueprint.route('/edit/<article_id>')
def edit(article_id=None):
    if article_id:
        article_info = Article.query.get(article_id)
        return render_template('blog_template/edit.html', article_info=article_info)
    else:
        return render_template('blog_template/edit.html', article_info={'title': '', 'content': ''})
