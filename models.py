from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "users.db")
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.String(), primary_key=True)
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

    @staticmethod
    def get(user_id):
        try:
            user = db.one_or_404(
                db.select(User).filter_by(id=user_id),
                description=f'No user {user_id} found'
            )
            return user
        except:
            print('went into except')
            return None

    @staticmethod
    def create(id_, name, email, profile_pic):
        user = User(id = id_, name = name, email=email, profile_image_url=profile_pic)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def update_recipes(new_recipe_book, user_id):
        with app.app_context():
            user = User.get(user_id)
            user.recipes = new_recipe_book
            db.session.commit()
