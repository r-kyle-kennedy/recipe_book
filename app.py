from flask import (render_template)
from flask_bootstrap import Bootstrap
from models import db, app, User


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/recipes/<id>')
def recipe_book(id):
    user = User.query.get_or_404(id)
    # recipes = user['Recipes']
    return render_template('recipe_book.html', user=user)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__=='__main__':
    Bootstrap(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
