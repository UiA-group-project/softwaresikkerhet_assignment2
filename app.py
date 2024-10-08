# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request
import sqlite3

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

# ----------------------------------------------------------------------------#
# DB Setup
# ----------------------------------------------------------------------------#
connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS post (id INTEGER PRIMARY KEY, title TEXT, content TEXT)"
)

cursor.execute(
    "INSERT INTO post (title, content) VALUES ('Vunerable Blog', 'This is a vunerable blog')"
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


@app.route("/vunerableblog")
def vunerableblog():
    return render_template("pages/vunerableblog.html")


@app.route("/secureblog")
def secureblog():
    return render_template("pages/secureblog.html")


@app.route("/posts", methods=["GET", "POST"])
def manage_posts():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        prepared_statement = (
            "INSERT INTO post (title, content) VALUES ('"
            + title
            + "', '"
            + content
            + "')"
        )
        cursor.execute(prepared_statement)
        connection.commit()
        return "Post created successfully", 201

    elif request.method == "GET":
        cursor.execute("SELECT * FROM post")
        posts = cursor.fetchall()
        return render_template("pages/posts.html", posts=posts)


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
