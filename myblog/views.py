import click
from flask import render_template, url_for, request
from myblog.models import Article
from myblog import app


@app.route('/', methods=['GET'])
def index(page=1):
    page = request.args.get('page', 1, type=int)
    if not page:
        page = 1
    articles = Article.query.filter().paginate(page=page, per_page=4)
    return render_template('index.html', articles=articles.items, pagination=articles)
