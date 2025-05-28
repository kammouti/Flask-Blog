from flask import Flask, render_template, flash, url_for, redirect, request,session
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from blog_forms import ArticleFrom, UserFrom, LoginFrom
from models import Article, User, db

load_dotenv()
secret_key = os.getenv("MY_KEY")
app = Flask(__name__)
#  Add db to the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# add secret key to the app
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Initialize the database
db.init_app(app)
# db = SQLAlchemy(app)

# migration instance
migrate = Migrate(app,db)

# Login:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))



# ################################ Public routes: ################################

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/articles")
def articles():
    articles = db.session.query(Article).order_by(Article.created_at).all()
    return render_template("articles.html", articles=articles)

@app.route("/articles/<int:id>")
def article(id):
    article = db.session.query(Article).get_or_404(id)
    return render_template("article.html", article=article)


# ################################ Article routes: ################################

@app.route("/add_article", methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleFrom()
    if form.validate_on_submit():
        exist = Article.query.filter_by(title=form.title.data).first()
        if exist is None:
            # add data to database
            article = Article(
            title = form.title.data,
            slug = form.slug.data,
            content = form.content.data,
            extrait = form.extrait.data,
            category = form.category.data
            )
            db.session.add(article)
            db.session.commit()
            flash(f'Article - {form.title.data} - ajoutee avec succee!', 'success')
            return redirect(url_for('articles'))
        else:
            flash("Titre de l'article exist deja! changer le titre ou verifier la liste des articles", 'error')
    return render_template("add_article.html", form=form)


@app.route("/edit_article/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_article(id):
    form = ArticleFrom()
    article_to_edit = Article.query.get_or_404(id)
    duplicate = Article.query.filter(Article.id != article_to_edit.id, Article.title==request.form.get('title'),).first()
    if request.method == "POST":
        article_to_edit.title = request.form.get('title')
        article_to_edit.slug = request.form.get('slug')
        article_to_edit.content = request.form.get('content')
        article_to_edit.extrait = request.form.get('extrait')
        article_to_edit.category = request.form.get('category')
        
        if duplicate:
            flash("Titre de l'article deja existe, essayez a nouveau!", 'message')
            return redirect(url_for('edit_article', id =id))
        else:
            try:
                db.session.commit()
                flash(f"Article - {article_to_edit.title} - modifiee avec succee", "success")
                return redirect(url_for('articles'))
            except:
                flash("Oups! un probleme est survenu, esseyer a nouveau!", "error")
                return redirect(url_for('edit_article', id =id))
    return render_template("edit_article.html", form=form, article_to_edit=article_to_edit)


@app.route("/delete_article/<int:id>")
@login_required
def delete_article(id):
    article_to_delete = Article.query.get_or_404(id)
    try:
        db.session.delete(article_to_delete)
        db.session.commit()
        flash("Article suprime avec succes.", "success")
        # return render_template("articles.html",
        #                        articles=articles)
        return redirect(url_for('articles'))
    except:
        flash("Oups! Esseyez a nouveau!", "error")
        # return render_template("articles.html",
        #                        articles=articles)
        return redirect(url_for('articles'))



# ################################ User routes: ################################

@app.route("/add_user", methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserFrom()
    # user_list = db.session.query(User).order_by(User.created_at).all()
    user_list = User.query.order_by(User.created_at).all()
    if form.validate_on_submit():
        user_exit = User.query.filter_by(username=form.username.data).first()
        if user_exit is None:
            # using password insted of password_hash so the password is hashed automaticly
            user_to_add = User(username = form.username.data,
                               password = form.password_hash.data,
                               full_name = form.full_name.data
                               )
            db.session.add(user_to_add)
            db.session.commit()
            flash("Utilisateur ajoute avec succes")
            return redirect(url_for('add_user'))
        else:
            flash("Non d'utilisateur deja exist")
    # clean up the fields
    form.username.data = ''
    form.full_name.data = ''
    form.password_hash.data = ''
    form.password_hash2.data = ''
    return render_template("add_user.html",
                           form=form,
                           user_list = user_list)


@app.route("/delete_user/<int:id>")
@login_required
def delete_user(id):
    form = UserFrom()
    user_list = User.query.order_by(User.created_at)
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Utilisateur suprime avec succes",)
        form.username.data = ''
        form.full_name.data = ''
        form.password_hash.data = ''
        # return render_template("add_user.html",
        #                        user_list=user_list,
        #                        form=form)
        return redirect(url_for('add_user'))
    except:
        flash("Oups! Esseyez a nouveau!")
        return redirect(url_for('add_user'))



# ################################ Login routes: ################################


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginFrom()
    if form.validate_on_submit():
        username = form.username.data
        password_hash = form.password_hash.data
        
        user_to_check = User.query.filter_by(username=username).first()
        if user_to_check:
            if user_to_check.verify_password(password_hash):
                login_user(user_to_check)
                flash('Utilisateur connecte avec succee!', "success")
                return redirect(url_for('articles'))
            else:
                flash('Mot de passe incorect!', "error")
        else:
            flash("Nom d'utilisateur n'exist pas!", "message")
        
    return render_template("login.html", form = form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/admin_dash/<username>")
def admin_dash(username):
    return render_template("admin.html", username=username)



# ################################ Error pages: ################################

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