from faker import Faker
from myblog.models import Article
from myblog import db

fake = Faker(locale="zh")


def fake_article(number):
    for i in range(number):
        article = Article(
            title=fake.sentence(),
            # title=fake.word(),
            content=fake.text(200)
        )
        db.session.add(article)
    db.session.commit()
