import random
from models import db, User, Article, Tag
from faker import Factory

user = User(username='leo', password='takeit')
db.session.add(user)
db.session.commit()

tag_one = Tag(name='Python')
tag_two = Tag(name='Flask')
tag_three = Tag(name='SQLALchemy')
tag_four = Tag(name='JMilkFan')
tag_list = [tag_one, tag_two, tag_three, tag_four]


fake = Factory.create()


for i in range(100):
        content = fake.text(2000)
        article = Article(title='title' + fake.text(20))
        article.user = user
        article.text = fake.text(2000)
        article.abstract = article.text[:200]
        article.tags = random.sample(tag_list, random.randint(1, 3))
        db.session.add(article)
db.session.commit()

