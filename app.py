import os
import requests
import json
import psycopg2
from flask import Flask, render_template, request, flash, redirect, session, jsonify, g, abort
from mypackage.models import Category, connect_db, db, Article, User, Favorite
from mypackage.forms import RegisterForm, LoginForm, DeleteForm, UserFavoriteArticleForm
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
from mypackage.apidata import SUPER_SECRET_KEY
API_SECRET_KEY = SUPER_SECRET_KEY

CURR_USER_KEY = "username"

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('data_url', 'postgresql:///capstone_database')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.filter_by(username=session[CURR_USER_KEY]).first()

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


##############################################################################################################
# API ROUTE BELOW HERE
####### route for query parameter ############
@app.route('/api/get_articles/query_data/<qvalue>')
def search_data(qvalue):
    response = requests.get("https://newsapi.org/v2/everything", params={'q':qvalue, 'apiKey':API_SECRET_KEY})
    res = response.json()
    return res


################### route for user #############
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """Returns JSON w/ a user"""
    user= User.query.get_or_404(user_id)
    return jsonify(user=user.user_serialize())



@app.route('/api/users', methods=["POST"])
def create_user():
    """Creates a new user and returns JSON of that created user"""
    data = request.json
    new_user = User.register(email=data["email"], 
                       username=data["username"],
                       password=data["password"],
                       image=data["image_url"]
    )
    db.session.add(new_user)
    db.session.commit()
    response_json = jsonify(user=new_user.user_serialize())
    return (response_json, 201)


@app.route('/api/users/<int:user_id>', methods=["PATCH"])
def update_user(user_id):
    """Updates a particular user and responds w/ JSON of that updated user"""
    user = User.query.get_or_404(user_id)
    user.email = request.json.get('email', user.email)
    user.username = request.json.get('username',  user.username)
    user.password = request.json.get('password',  user.password)
    user.image_url = request.json.get('image_url',  user.image_url)
    db.session.commit()
    return jsonify(user=user.user_serialize())

@app.route('/api/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    """Deletes a particular user"""
    user = Article.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="Deleted")

###################### ('/api/users/<int:user_id>/categories')####################
@app.route('/api/categories')
def list_categories():
    """Returns JSON w/ all categories"""
    category = [category.category_serialize() for category in Category.query.all()]
    return jsonify(categories=category)

@app.route('/api/categories/<int:cate_id>')
def get_category(cate_id):
    """Returns JSON for one category in particular"""
    category = Category.query.get_or_404(cate_id)
    return jsonify(category=category.category_serialize()) 

@app.route('/api/categories', methods=["POST"])
def create_category():
    """Creates a new category and returns JSON of that created category"""
    data = request.json
    new_category = Category(name=data["name"])

    db.session.add(new_category)
    db.session.commit()
    response_json = jsonify(category=new_category.category_serialize())
    return (response_json, 201)

@app.route('/api/categories/<int:category_id>', methods=["PATCH"])
def update_category(category_id):
    """Updates a particular category and responds w/ JSON of that updated category"""
    category = Category.query.get_or_404(category_id)
    category.name = request.json.get('name', category.name)
    db.session.commit()
    return jsonify(category=category.serialize())


@app.route('/api/categories/<int:category_id>', methods=["DELETE"])
def delete_category(category_id):
    """Deletes a particular category"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(message="Deleted")

#################################################################################################
#######getting an artcile###########
@app.route('/api/articles/<int:article_id>')
def get_article(article_id):
    """Returns JSON for one article in particular"""
    article = Article.query.get_or_404(article_id)
    return jsonify(article=article.article_serialize())

############getting articles for a specific category############
@app.route('/api/categories/<int:cate_id>/articles')
def list_articles(cate_id):
    """Returns JSON w/ all articles"""
    category = Category.query.get(cate_id)
    article_for_category = category.category_article
    all_articles = [article.article_serialize() for article in article_for_category]
    return jsonify(articles=all_articles)



@app.route('/api/categories/<int:cate_id>/articles', methods=["POST"])
def create_article():
    """Creates a new article and returns JSON of that created article"""
    data = request.json
    new_article = Article(author=data["author"], 
                       title=data["title"],
                       description=data["description"],
                       url=data["url"],                       
                       published_date=data["published_date"],
                       content=data["content"])

    db.session.add(new_article)
    db.session.commit()
    response_json = jsonify(article=new_article.serialize())
    return (response_json, 201)

@app.route('/api/categories/<int:cate_id>/articles/<int:article_id>', methods=["PATCH"])
def update_article(article_id):
    """Updates a particular article and responds w/ JSON of that updated article"""
    article = Article.query.get_or_404(article_id)
    article.author = request.json.get('author', article.author)
    article.title = request.json.get('title',  article.title)
    article.description = request.json.get('description',  article.description)
    article.url = request.json.get('url',  article.url)
    article.published_date = request.json.get('published_date',  article.published_date)
    article.content = request.json.get('content',  article.content)
    db.session.commit()
    return jsonify(articles=article.serialize())


@app.route('/api/categories/articles/<int:article_id>', methods=["DELETE"])
def delete_article(article_id):
    """Deletes a particular article"""
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify(message="Deleted")



#################################################################################################

# FLASK APP ROUTE BELOW HERE

@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    category = Category.query.all()
    article = Article.query.all()
    return render_template('index.html', article=article, category=category)
    # return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect("/article")

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            email = form.email.data
            username = form.username.data
            image_url = form.image_url.data
            password = form.password.data  
            user = User.register(email, username, password, image_url)
            db.session.commit()
            session['username'] = user.username

        except IntegrityError as e:
            flash("Username already taken.", 'danger')            
            return render_template("user/register.html", form=form)

        flash("Signup successful.", 'success') 
        return redirect("/login")


    else:
        return render_template("user/register.html", form=form) 



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect("article")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            flash(f"Hello, {user.username}!", "success")
            return redirect(f"/category")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("user/login.html", form=form)

    return render_template("user/login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    
    # session.pop("username")

    flash("You have successfully logged out.", 'success')
    return redirect("/")



@app.route('/article')
def show_article():
    if "username" not in session:
        raise Unauthorized()
    username = session['username']
    article = Article.query.all()
    user = User.query.filter_by(username=username).first()
    favart = Favorite.query.filter_by(user_id=user.id)
    found_article = [a.favoriteArticle_id for a in favart]
    category = Category.query.all()
    return render_template('index.html', article=article, category=category, favart=favart, found_article=found_article)


@app.route('/category')
def show_categories():
    category = Category.query.all()
    return render_template('category/show.html', category=category)

@app.route('/category/<int:cat_id>')
def show_category(cat_id):
    if "username" not in session:
        raise Unauthorized()
    username = session['username']
    category = Category.query.get(cat_id)
    catart = category.category_article
    user = User.query.filter_by(username=username).first()
    favart = Favorite.query.filter_by(user_id=user.id)
    found_article = [a.favoriteArticle_id for a in favart]
    return render_template('article/show.html', allarticle=catart, cat=category, favart=favart, found_article=found_article)


@app.route('/users/favorites/<username>')
def favorite_page(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.filter_by(username=username).first()
    # article = Favorite.query.filter_by(user_id=user.id)
    article = user.user_article
    return render_template("/user/favorites.html", 
                            article=article, user=user)

# @app.route('/users/favorite/<int:article_id>', methods=['POST'])
# def add_article_to_favorite(article_id):
#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")
#     article = Article.query.get_or_404(article_id)
#     username = g.user
#     user = User.query.filter_by(username=username).first()
#     user_id = user.id
#     u_a = Favorite(user_id=1, article_id=article_id)
#     db.session.add(u_a)
#     db.session.commit()
#     g.user.user_article.append(article)
#     return redirect(f"/users/favorites/{g.user}")


@app.route("/users/favorites/add_article/<username>", methods=["GET", "POST"])
def add_song_to_playlist(username):
    """Handle add-article to favorite form:"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.filter_by(username=username).first()
    user_id = user.id   
    form = UserFavoriteArticleForm()

#   # Restrict form to article not already on this favorite

    # curr_on_favorite = [s.title for s in user.user_article]
    form.article.choices = (1)
    # form.article.choices = (db.session.query(Article.title))
                    #   .filter(Article.title.notin_(curr_on_favorite))
                    #   .all())

    # if form.validate_on_submit():     
    #     favorite_article = Favorite(user_id=user_id,
    #                               article_id=form.article.data)
    #     db.session.add(favorite_article)
    #     db.session.commit()
    #     return redirect(f"/favorites/{username}")

    return render_template("user/add_favorite.html",
                        #  user=user,
                         form=form)




@app.route('/favorites/articles/<int:id>')
def add_favorite(id):
    """Creates a new article and returns JSON of that created article"""
    if "username" not in session:
        raise Unauthorized()
    username = session['username']
    user = User.query.filter_by(username=username).first()    
    favart =  user.user_article 
    found_article = [a.id for a in favart]
    article = Favorite.query.filter_by(favoriteArticle_id=id).filter_by(user_id=user.id).first()
    if id in found_article:
        db.session.delete(article)
        db.session.commit()    
    else:
        new_fav = Favorite(user_id=user.id, 
                       favoriteArticle_id=id
                       )
        db.session.add(new_fav)
        db.session.commit()

    return redirect (f"/users/favorites/{username}")


API_BASE_URL = "https://newsapi.org/v2"

res = requests.get(f"{API_BASE_URL}/top-headlines/sources",
                        params={'apiKey':API_SECRET_KEY})