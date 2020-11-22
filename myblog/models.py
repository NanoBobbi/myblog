from myblog import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    # date = db.Column(db.Date)
    content = db.Column(db.Text)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(10))
    password = db.Column(db.String(10))
