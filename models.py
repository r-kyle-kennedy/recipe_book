from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_database_uri():
    database_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    db_path = os.path.join(BASE_DIR, "users.db")
    return "sqlite:///" + db_path


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
