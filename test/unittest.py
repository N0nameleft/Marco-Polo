import unittest, os
from application.project import app, db, models
from application.project.models import User

class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client()
        db.create_all()
        user1 = User(id=9999, username="FirstTest", email="test-u1@peaksandtroughs.com")
        user2 = User(id=9998, username="SecondTest", email="test-u2@peaksandtroughs.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
