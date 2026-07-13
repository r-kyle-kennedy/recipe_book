from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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
