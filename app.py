from flask import Flask, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_article")
def add_article():
    return render_template("add_article.html")

@app.route("/articles")
def articles():
    return render_template("articles.html")


@app.route("/admin/<username>")
def admin(username):
    return render_template("admin.html", username=username)


# Costum error pages:

# invalid URL
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# Internal server error
@app.errorhandler(500)
def not_found(e):
    return render_template("500.html"), 500




if __name__ == "__main__":
    app.run(debug=True)