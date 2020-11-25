from wtforms import  TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class ArticleForm(FlaskForm):
    body = TextAreaField('body', [DataRequired()])