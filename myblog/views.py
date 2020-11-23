import click
from flask import render_template, url_for, request
from myblog.models import Article, Category
from myblog import app


@app.route('/', methods=['GET'])
def index(page=1):
    page = request.args.get('page', 1, type=int)
    if not page:
        page = 1
    articles = Article.query.filter().order_by(Article.timestamp.desc()).paginate(page=page, per_page=4)
    categories = Category.query.all()
    return render_template('index.html', articles=articles.items, pagination=articles, categories=categories)


@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def show_article(article_id):
    article = Article.query.get_or_404(article_id)
    categories = Category.query.all()
    return render_template('article.html', article=article, categories=categories)


@app.route('/category/<int:category_id>', methods=['GET', 'POST'])
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.with_parent(category).order_by(Article.timestamp.desc()).paginate(page, per_page=4)
    articles = pagination.items
    return render_template('category.html', category=category, categories=categories, articles=articles,
                           pagination=pagination)
