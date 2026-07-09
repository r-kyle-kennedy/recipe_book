from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String())
    recipes = db.Column('Recipes', db.JSON())

    def __repr__(self):
        return f'''User (name: {self.name}
                recipes: {self.recipes}
                id: {self.id}'''

# class Recipe(db.Model):
#     id = db.mapped_column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer)
#     name = db.Column('Name', db.string())
#
#     def __repr__(self):
#         return f'''Recipe (name: {self.name}
#                 id: {self.id}'''
#
#
# class Ingrediant(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     recipe_id = db.Column(db.Integer)
#     name = db.Column('Name', db.string())
#     url = db.Column('Url', db.String())
