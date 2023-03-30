from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    """
    使用装饰器注册一个错误处理函数，作用和视图函数类似，当404错误发生时就会触发
    返回值作为相应主体返回客户端
    """
    # 后跟status_code
    return render_template('404.html', user='zhangsan'), 404


@app.route('/')
def index():
    return render_template('index.html')
