from datetime import datetime, timezone

import click
from click import echo
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from myblog.models import Article, Category, User
from myblog import app, db
from flask_sqlalchemy import SQLAlchemy, Model


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
def admin_index(string=None):
    return render_template('admin/admin_index.html', string="hello, None")


@app.route('/admin/admin_categories')
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/admin_categories.html', categories=categories)


@app.route('/admin/add_category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['category']
        categories = Category.query.all()
        for category in categories:
            if category.name == category_name:
                return redirect(url_for('admin_categories'))
        category = Category(name=category_name)
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    flash("Add category succeed!")
    return redirect(url_for('admin_categories'))


@app.route('/admin/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    category.delete()
    flash("Delete category succeed!")
    return render_template('admin/admin_index.html', string="Delete category successfully!")


@app.route('/admin/admin_articles')
def admin_articles():
    # articles = Article.query.all()
    # categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter().order_by(Article.timestamp.desc()).paginate(page, per_page=5)
    articles = pagination.items
    return render_template('admin/admin_articles.html', articles=articles, pagination=pagination)


@app.route('/admin/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash("Delete article succeed!")
    return redirect(url_for("admin_articles"))


@app.route('/admin/add_article', methods=['POST', 'GET'])
def add_article():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form['title']
        category_id = request.form['category_id']
        content = request.form['content']
        echo(title)
        article = Article(title=title, category_id=category_id, content=content)
        db.session.add(article)
        db.session.commit()
        flash("Add article succeed!")
        return render_template('admin/admin_index.html', string="Add article successfully!")
    return render_template('admin/add_article.html', categories=categories)


@app.route('/admin/edit/<int:article_id>', methods=['POST', 'GET'])
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    categories = Category.query.all()
    if request.method == 'POST':
        article.title = request.form['title']
        article.category_id = request.form['category_id']
        article.content = request.form['content']
        article.timestamp = datetime.now()
        db.session.commit()
        flash("Edit article succeed!")
        return render_template('admin/admin_index.html', string="edit successfully")
    return render_template('admin/add_article.html', article=article, categories=categories)


@app.route('/admin/login', methods=['POST', 'GET'])
def login():
    from flask_login import current_user
    if not current_user.is_authenticated:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.first()
            if user.userName == username and user.password == password:
                from flask_login import login_user
                login_user(user)
                flash('Logged Succeed!')
                return render_template('admin/admin_index.html', string="hello %s" % username)
            else:
                flash('Invalid username or password!')
                return render_template('admin/login.html')

    else:
        flash('Welcome back')
        return render_template('admin/admin_index.html', string="hello again ")
    return render_template('admin/login.html')


@app.route('/admin/logout')
# @login_required
def logout():
    from flask_login import logout_user
    logout_user()
    flash("Logout!")
    return render_template('admin/login.html')
