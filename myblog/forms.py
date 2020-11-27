from wtforms import TextAreaField, TextField
from flask_wtf import FlaskForm, Form
from wtforms.validators import DataRequired


class ArticleForm(Form):
    title = TextField("title of article")
