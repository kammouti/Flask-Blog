from flask import Flask, render_template, flash, url_for
from dotenv import load_dotenv
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

load_dotenv()
secret_key = os.getenv("MY_KEY")
app = Flask(__name__)
#  Add db to the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# add secret key to the app
app.config['SECRET_KEY'] = secret_key
#  Initialize the database
db = SQLAlchemy(app)


# creating Models
# class Article(db.Model):
#     id = 
#     title = 
#     extrait = 
#     content = 
#     category = 
#     created_at = 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # create a string
    def __repr__(self):
        return '<Username %r>' % self.username

# create a form class
class ArticleFrom(FlaskForm):
    title = StringField("Titre de l'article", validators=[DataRequired()])
    extrait = TextAreaField("Extrait de l'article", validators=[DataRequired()])
    content = TextAreaField("Contenu de l'article", validators=[DataRequired()])
    category = SelectField("Categorie",validators=[DataRequired()],choices=["Lois de conduite","General", "Lois au Maroc", "Technique de conduite", "Evenement"])
    submit = SubmitField("Ajouter")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_article", methods=['GET', 'POST'])
def add_article():
    form = ArticleFrom()
    if form.validate_on_submit():
        # add data to database
        title = form.title.data
        content = form.content.data
        extrait = form.extrait.data
        category = form.category.data
        flash('Article ajouter avec succee!')
        return render_template("articles.html")
    return render_template("add_article.html", form = form)

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