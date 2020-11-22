from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sys
import os

# 寻找跟目录
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 实例化 一个app
app = Flask(__name__)

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 让flask找到sqlite3的数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

# def create_app():
#     app = Flask(__name__)

# 实例化 一个数据库连接
db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def loader_user(user_id):
#     from models import User
#     user = User.query.first(int(user_id))
#     return user
#
#
# @app.context_processor
# def inject_user():
#     from models import User
#     user = User.query.first()
#     return dict(user=user)


# if __name__ == '__main__':
#     app.run()


from myblog.commands import register_commands
# 注册所有的终端命令，每次开启前都需要在终端输入命令export FLASK_APP=myblog 才能奏效

register_commands()
# 避免循环依赖
from myblog import commands, models, views
