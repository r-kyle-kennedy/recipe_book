import os
import unittest

from models import get_database_uri


class DatabaseConfigTests(unittest.TestCase):
    def test_uses_render_database_url_when_present(self):
        original = os.environ.get("DATABASE_URL")
        os.environ["DATABASE_URL"] = "postgresql://user:pass@host:5432/db"
        try:
            self.assertEqual(get_database_uri(), "postgresql://user:pass@host:5432/db")
        finally:
            if original is None:
                os.environ.pop("DATABASE_URL", None)
            else:
                os.environ["DATABASE_URL"] = original

    def test_falls_back_to_sqlite_when_no_database_url_is_set(self):
        original = os.environ.get("DATABASE_URL")
        os.environ.pop("DATABASE_URL", None)
        try:
            uri = get_database_uri()
            self.assertTrue(uri.startswith("sqlite:///"))
        finally:
            if original is None:
                os.environ.pop("DATABASE_URL", None)
            else:
                os.environ["DATABASE_URL"] = original


if __name__ == "__main__":
    unittest.main()
