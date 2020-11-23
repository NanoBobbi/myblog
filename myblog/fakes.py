
from faker import Faker
from faker.generator import random
from sqlalchemy.exc import IntegrityError

from myblog.models import Article, Category
from myblog import db

fake = Faker(locale="zh")


def fake_categories(count=10):
    category = Category(name='Default')

    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_article(number):
    for i in range(number):
        article = Article(
            title=fake.sentence(5),
            # title=fake.word(),
            content=fake.text(200),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(article)
    db.session.commit()
