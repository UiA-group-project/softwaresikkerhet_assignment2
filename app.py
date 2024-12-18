# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, make_response
import sqlite3

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

# ----------------------------------------------------------------------------#
# DB Setup
# ----------------------------------------------------------------------------#
connection = sqlite3.connect("database.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS post (id INTEGER PRIMARY KEY, title TEXT, content TEXT)"
)

connection.commit()

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object("config")
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
"""
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
"""

# Login required decorator.
"""
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
"""

# ----------------------------------------------------------------------------#
# DB requests.
# ----------------------------------------------------------------------------#

def getAllPosts():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    return posts

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def home():
    return render_template("pages/placeholder.home.html")


@app.route("/about")
def about():
    return render_template("pages/placeholder.about.html")


@app.route("/login")
def login():
    form = LoginForm(request.form)
    return render_template("forms/login.html", form=form)


@app.route("/register")
def register():
    form = RegisterForm(request.form)
    return render_template("forms/register.html", form=form)


@app.route("/forgot")
def forgot():
    form = ForgotForm(request.form)
    return render_template("forms/forgot.html", form=form)


@app.route("/vunerableblog", methods=["GET", "POST"])
def vunerableblog():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        # Also vunerable to SQL injection
        sqlstatement = f"INSERT INTO post (title, content) VALUES ('{title}', '{content}')"
        cursor.execute(sqlstatement)
        connection.commit()
    posts = getAllPosts()
    return render_template("pages/vunerableblog.html", posts=posts)


@app.route("/secureblog", methods=["GET", "POST"])
def secureblog():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        sqlstatement = "INSERT INTO post (title, content) VALUES (?, ?)"
        cursor.execute(sqlstatement, (title, content))
        connection.commit()
    posts = getAllPosts()
    
    # Add CSP header for the secure blog page
    response = make_response(render_template("pages/secureblog.html", posts=posts))
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self';"
    return response

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template("errors/500.html"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run(debug=True)

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
