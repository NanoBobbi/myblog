from datetime import datetime
from myblog import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    articles = db.relationship('Article', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        articles = self.articles[:]
        for article in articles:
            article.category = default_category
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    # date = db.Column(db.Date)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='articles')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(10))
    password = db.Column(db.String(10))
