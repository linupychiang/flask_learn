from mongoengine import Document, StringField, IntField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(Document, UserMixin):
    """
    继承UserMixin会让User类拥有几个用于判断认证状态的属性和方法
    其中最常用的是is_authenticated属性：
    如果当前用户已登录，current_user.is_authenticated返回True，否则返回False
    有了current_user变量和这几个验证方法和属性，可以轻松判断当前用户的认证状态
    """
    name = StringField(required=True)
    password_hash = StringField(required=True)
    meta = {'verbose': '用户表', 'collection': 'user'}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(Document):
    title = StringField(required=True)
    year = IntField(min_value=1000, max_value=9999, required=True)
    meta = {'verbose': '电影表', 'collection': 'movie'}


# 创建用户可通过 `flask shell` 执行相关代码创建
'''
from app import User
user = User(name='zhangsan')
user.set_password('zhangsan')
user.save()
'''
