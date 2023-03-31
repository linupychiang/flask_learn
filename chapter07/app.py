from flask import Flask, flash, request, url_for, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

db_flask_demo = PyMongo(
    app,
    uri='mongodb://admin:12345678@localhost:27017/flask_demo?authSource=admin')


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
    user = db_flask_demo.db.user.find_one({}, {'_id': 0})
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
        db_flask_demo.db.movie.insert_one({'title': title, 'year': year})
        flash('item created')
        return redirect(url_for('index'))

    movies = db_flask_demo.db.movie.find({}, {'_id': 0})
    movies = [movie for movie in movies]
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<string:title>', methods=['GET', 'POST'])
def edit_movie(title):
    movie = db_flask_demo.db.movie.find_one({'title': title}, {'_id': 0})
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(title) > 50 or len(year) > 4:
            flash('Invalid input...')
            return redirect(url_for('edit_movie', title=title))

        db_flask_demo.db.movie.update_one(
            {'title': movie['title']},
            {'$set': {
                'title': title,
                'year': int(year)
            }})
        flash('update finished')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)
