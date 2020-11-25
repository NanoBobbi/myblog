import click
from flask import render_template, url_for, request
from myblog.models import Article, Category
from myblog import app, db


@app.route('/', methods=['GET'])
def index(page=1):
    page = request.args.get('page', 1, type=int)
    if not page:
        page = 1
    pagination = Article.query.filter().order_by(Article.timestamp.desc()).paginate(page=page, per_page=4)
    categories = Category.query.all()
    return render_template('index.html', articles=pagination.items, pagination=pagination, categories=categories)


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


@app.route('/admin')
def admin_index():
    return render_template('admin/admin_index.html')


@app.route('/admin/all_articles')
def all_articles():
    # articles = Article.query.all()
    # categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter().order_by(Article.timestamp.desc()).paginate(page, per_page=5)
    articles = pagination.items
    return render_template('admin/all_articles.html', articles=articles, pagination=pagination)


@app.route('/admin/all_categories')
def all_categories():
    categories = Category.query.all()
    return render_template('admin/all_categories.html', categories=categories)


@app.route('/admin/add_article')
def add_article():
    return render_template('admin/add_article.html')


@app.route('/admin/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    # flash("dele")
    from flask import redirect
    return redirect(url_for("all_articles"))


@app.route('/admin/edit/<int:article_id>', methods=['POST', 'GET'])
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('admin/add_article.html', article=article)
