import json
import os
import sqlite3
from urllib.request import urlopen
from flask import Flask, redirect, request, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_bootstrap import Bootstrap
from models import db, app, User
from dotenv import load_dotenv

load_dotenv()
#set to dasable https, remove for launch
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
RECIPEAPI_KEY = os.environ.get("RECIPEAPI_KEY", None)

app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route('/login')
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    # print(request_uri)
    return redirect(request_uri)

@app.route('/login/callback')
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400


    # Create a user in your db with the information provided
    # by Google
    user = User(id=unique_id, name=users_name, email=users_email, profile_image_url=picture)
    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        print('created user')
        User.create(unique_id, users_name, users_email, picture)



    # Begin user session by logging the user in
    if login_user(user):
        print('logged in')
    else:
        print('not logged in')

    # Send user back to homepage
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(401)
def page_not_found(e):
    return redirect('/')

@app.route('/new')
def new_recipe():
    if current_user.is_active:
        return render_template('new_recipe.html')
    else:
        return redirect('/login')

@app.route('/recipes')
def recipe_book():
    try:
        recipes = User.query.get_or_404(current_user.id).recipes
        return render_template('recipe_book.html', recipes=recipes)
    except Exception as e:
        print(e, 'in recipe book function')
        return redirect('/login')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recipe/new', methods=['POST','GET'])
def add_recipe():
    if request.form:
        # dynamically make ingredient dictionary for db
        ingredients={}
        ingredient_names=[]
        ingredient_amounts=[]
        ingredient_urls=[]
        ingredient_calories=[]
        ingredient_protein=[]
        ingredient_fat=[]
        ingredient_carbs=[]
        total_cal_counter=0
        for key, value in request.form.items():
            if key.startswith('ingredient'):
                ingredient_names.append(value)
            elif key.startswith('amount'):
                ingredient_amounts.append(value)
            elif key.startswith('url'):
                ingredient_urls.append(value)
            elif key.startswith('calories'):
                ingredient_calories.append(value)
                total_cal_counter+=int(value)
            elif key.startswith('protein'):
                ingredient_protein.append(value)
            elif key.startswith('fat'):
                ingredient_fat.append(value)
            elif key.startswith('carbs'):
                ingredient_carbs.append(value)
        for n in range(0, len(ingredient_names)):
            ingredients[ingredient_names[n]] = {
                "amount" : ingredient_amounts[n],
                "calories" : int(ingredient_calories[n]),
                "url" : ingredient_urls[n],
                "macros" :
                    {
                    "protein" : int(ingredient_protein[n]),
                    "fat" : int(ingredient_fat[n]),
                    "carbs" : int(ingredient_carbs[n])
                    }
            }
        recipes = User.query.get_or_404(current_user.id).recipes
        edit_name = request.form['name'].replace(' ', '_')
        recipes.update({edit_name : {
            'name' : request.form['name'],
            'ingredients' : ingredients,
            'directions' : request.form['directions'],
            'servings': int(request.form['servings']),
            'totalCal': total_cal_counter
        }})
        User.update_recipes(recipes, current_user.id)
    return redirect(url_for('recipe_book'))

@app.route('/recipe/delete/<recipe_key>', methods=['POST','GET'])
def delete_recipe(recipe_key):
    recipes = User.query.get_or_404(current_user.id).recipes
    recipes.pop(recipe_key)
    User.update_recipes(recipes, current_user.id)
    return redirect(url_for('recipe_book'))


@app.route('/recipe/edit/<recipe_key>', methods=['POST','GET'])
def edit_recipe(recipe_key):
    recipe_key = recipe_key.replace(' ', '_')
    recipes = User.query.get_or_404(current_user.id).recipes
    if request.form:
        recipes.pop(recipe_key)
        User.update_recipes(recipes, current_user.id)
        add_recipe()
        return redirect(url_for('recipe_book'))
    return render_template('edit_recipe.html', recipe=recipes[recipe_key])

@app.route('/search', methods=['GET', 'POST'])
def search_new_recipe():
    if request.form:
        try:
            response = requests.get(
                "https://recipeapi.io/api/v1/recipes",
                params={"search": request.form['search']},
                headers={"Authorization": f"Bearer {RECIPEAPI_KEY}"}
            )

            data = response.json()
            return render_template('search_results.html', recipes=data['data'])
        except Exception as e:
            raise


    return render_template('index.html')

if __name__=='__main__':
    Bootstrap(app)
    with app.app_context():
        db.create_all()
    # get_user()
    app.run(debug=True, port=5000)
