from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

db_flask_demo = PyMongo(
    app,
    uri='mongodb://admin:12345678@localhost:27017/flask_demo?authSource=admin')


@app.route('/')
def get_index():
    users = db_flask_demo.db.user.find({}, {'_id': 0})
    movies = db_flask_demo.db.movie.find({}, {'_id': 0})
    user = users[0]['name']
    movies = [movie for movie in movies]
    return render_template('index.html', name=user, movies=movies)
