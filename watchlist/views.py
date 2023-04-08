from flask import request, flash, url_for, render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Movie
from . import app


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
