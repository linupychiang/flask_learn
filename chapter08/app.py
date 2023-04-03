from flask import Flask, flash, render_template, redirect, url_for
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import MongoEngine
from mongoengine import Document, StringField, IntField

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


class User(Document, UserMixin):
    name = StringField(required=True)
    password_hash = StringField(required=True)
    meta = {'verbose': '用户表', 'collection': 'user'}


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
    user = User.objects.filter().first()
    # user = db_flask_demo.db.user.find_one({}, {'_id': 0})
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
def delete_movie(title):
    Movie.objects(title=title).delete()
    flash('delete finished')
    return redirect(url_for('index'))
