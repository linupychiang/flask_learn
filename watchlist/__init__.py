from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from .models import User

app = Flask(__name__)
db = MongoEngine()

app.config['SECRET_KEY'] = 'dev'

# 待验证，连接消息无效
# app.config['MONGODB_SETTINGS'] = [{
#     'db': 'flask_demo',
#     'host': 'localhost',
#     'port': 27017,
#     'username': 'admin',
#     'password': '12345678',
# }]

app.config['MONGODB_SETTINGS'] = {
    'host':
    'mongodb://admin:12345678@localhost:27017/flask_demo?authSource=admin'
}
db.init_app(app)
login_manager = LoginManager(app)

# 设置程序的登录视图端点（函数名）
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    当程序运行后，如果用户已登录
    current_user 变量的值会是当前用户的用户模型类记录
    """
    user = User.objects(pk=user_id).first()  # id 非_id非user_id
    return user


@app.context_processor
def inject_user():
    """
    使用装饰器注册一个模版上下文处理函数
    """
    user = User.objects().first()
    # 函数返回的变量（以字典键值对的形式），
    # 将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用
    return {'user': user}


# 避免循环依赖
from . import errors, commands, views
