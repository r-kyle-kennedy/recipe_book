from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Name', db.String())
    email = db.Column('Email', db.String())
    profile_image_url = db.Column('ProfileImageUrl', db.String())
    recipes = db.Column('Recipes', db.JSON())

    def __repr__(self):
        return f'''User (name: {self.name}
                recipes: {self.recipes}
                id: {self.id}
                email: {self.email}
                profile_image_url: {self.profile_image_url}'''
