from flask import Flask, flash, render_template, redirect, url_for
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, IntField
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user, login_required, current_user

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
"""
当遇到需要login_required视图时，如何未登录状态下，会提示：
Please log in to access this page.
且视图更改为login_view(login页面)
"""


@login_manager.user_loader
def load_user(user_id):
    """
    当程序运行后，如果用户已登录
    current_user 变量的值会是当前用户的用户模型类记录
    """
    user = User.objects(pk=user_id).first()  # id 非_id非user_id
    return user


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('invalid input')
            return redirect(url_for('login'))
        user = User.objects(name=username).first()
        if not user:
            flash('null username')
            return redirect(url_for('login'))
        if username == user.name and user.validate_password(password):
            login_user(user)
            flash('login success')
            return redirect(url_for('index'))
        flash('wrong username or wrong password')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()
    flash('good bye')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    用户数据展示/修改
    """
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('invalid name')
            return redirect(url_for('settings'))
        current_user.name = name
        current_user.save()  # 修改数据入库

        flash('settings updated')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.errorhandler(404)
def page_not_found(e):
    """
    使用装饰器注册一个错误处理函数，作用和视图函数类似，当404错误发生时就会触发
    返回值作为相应主体返回客户端
    """
    # 后跟status_code
    return render_template('404.html'), 404


@app.context_processor
def inject_user():
    """
    使用装饰器注册一个模版上下文处理函数
    """
    user = User.objects().first()
    # 函数返回的变量（以字典键值对的形式），
    # 将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用
    return {'user': user}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(title) > 50 or len(year) > 4:
            flash('Invalid input...')
            return redirect(url_for('index'))
        # 数据更新逻辑
        # Movie(title=title, year=year).save()  # 两种写法
        Movie.objects().insert(Movie(title=title, year=year))
        flash('item created')
        return redirect(url_for('index'))

    movies = Movie.objects()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<string:title>', methods=['GET', 'POST'])
@login_required
def edit_movie(title):
    movie = Movie.objects(title=title).first()

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(title) > 50 or len(year) > 4:
            flash('Invalid input...')
            return redirect(url_for('edit_movie', title=title))
        Movie.objects(title=movie.title).update(set__title=title,
                                                set__year=year)
        flash('update finished')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<string:title>', methods=['POST'])
@login_required  # 登录保护
def delete_movie(title):
    Movie.objects(title=title).delete()
    flash('delete finished')
    return redirect(url_for('index'))
