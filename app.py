from flask import (Flask, render_template)
from flask_bootstrap import Bootstrap

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/recipes')
def recipe_book():
    return render_template('recipe_book.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__=='__main__':
    Bootstrap(app)
    app.run(debug=True)
