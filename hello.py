from datetime import datetime
from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internval_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    # user_agent = request.headers.get('User-Agent')
    # return '<h1>Your browser is %s</h1>' % user_agent
    return render_template('index.html',
                           current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
