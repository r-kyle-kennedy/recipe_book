import unittest

from models import User, db
from app import app


class RecipeStorageTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_new_user_starts_with_empty_recipe_collection(self):
        with self.app.app_context():
            User.create("user-1", "Test User", "test@example.com", "https://example.com/pic.png")
            stored_user = User.query.get("user-1")
            self.assertEqual(stored_user.recipes, {})


if __name__ == "__main__":
    unittest.main()
