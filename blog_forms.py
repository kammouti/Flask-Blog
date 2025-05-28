from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime



# create an article form class
class ArticleFrom(FlaskForm):
    title = StringField("Titre de l'article", validators=[DataRequired()])
    slug = StringField("Slug de l'article", validators=[DataRequired()])
    extrait = TextAreaField("Extrait de l'article", validators=[DataRequired()])
    content = TextAreaField("Contenu de l'article", validators=[DataRequired()])
    category = SelectField("Categorie",validators=[DataRequired()],choices=["General", "Lois de conduite", "Lois au Maroc", "Technique de conduite", "Evenement"])
    submit = SubmitField("Soumettre")


# user form class
class UserFrom(FlaskForm):
    full_name = StringField("Nom Complet")
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password_hash = PasswordField("Mot de passe", validators=[DataRequired(), EqualTo('password_hash2', message='Les mots de passe doivent correspondre!')])
    password_hash2 = PasswordField("Confirmer le Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# login form class
class LoginFrom(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password_hash = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Login")