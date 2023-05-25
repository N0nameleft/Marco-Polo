import unittest, os
from app import app, db, models, create_app
from app.models import User
from os.path import dirname
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from app.decisionMaking import *


class UserModelCase(unittest.TestCase):
    # def setUp(self):
    #     based = os.path.abspath(os.path.dirname(__file__))
    #     dbpath = os.path.join(based, "test.sqlite")
    #     conn = sqlite3.connect(dbpath)
    #     cur = conn.cursor()
    #     cur.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY, email TEXT, password TEXT, username TEXT)")
    #     cur.execute("INSERT INTO user VALUES(1001,'test1@mail.com','%s','Test1')" % generate_password_hash("test1", method="sha256"))
    #     cur.execute("INSERT INTO user VALUES(1002,'test2@mail.com','%s','Test2')" % generate_password_hash("test2", method="sha256"))
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = create_app
        db.init_app(self.app)
        with app.app_context():
            db.create_all()
        user1 = User(id=1001, username="Test1", email="test1@mail.com")
        user2 = User(id=1002, username="Test2", email="test2@mail.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u1 = User.query.get(1001)
        u2 = User.query.get(1002)
        u1.password = generate_password_hash("test1")
        u2.password = generate_password_hash("test2")
        self.assertFalse(check_password_hash(u1.password, 'test2'))
        self.assertFalse(u1.password == "test1")
        self.assertTrue(check_password_hash(u2, 'test2'))
        self.assertFalse(u2 == "test2")

    def test_username(self):
        self.assertTrue(str(Users.query.get(1001)) == "Test1")
        self.assertFalse(str(Users.query.get(1002)) == "Test1")

class algoCase(unittest.TestCase):
    def setUp(self):
        based = os.path.abspath(os.path.dirname(__file__))
        dbpath = os.path.join(based, "test_country.db")
        self.conn = sqlite3.connect(dbpath)
        self.cur = self.conn.cursor()
        self.table = 'completedata'
        countQuery = "SELECT COUNT(*) FROM %s" % self.table
        self.cur.execute(countQuery)
        self.rowCount = self.cur.fetchone()[0]
    
        self.column = getColumnNames(self.cur, self.table)
        self.assertTrue(getColumnNames(self.cur, self.table))
        self.assertTrue(countOne(self.cur, self.table, self.column[1]))
        self.assertTrue(countOne(self.cur, self.table, self.column[12]))

    def tearDown(self):
        self.cur.close()
        self.conn.close()
    
    def test_time(self):
        time1 = '20230102045533'
        time2 = '20001231235959'
        self.assertTrue(format_time(time1) == "02 Jan 2023, 04:55:33")
        self.assertTrue(format_time(time2) == "31 Dec 2000, 23:59:59")
    
    def test_finish_message(self):
        yes = 'yes'
        no = "no"
        self.assertTrue(game_finish(yes)['next_question_text'] == "Found ya! Do you want to start a new game?")
        self.assertTrue(game_finish(no)['next_question_text'] == "You win! Sorry I can't find you.\nDo you want to start a new game?")

    def test_percentage(self):
        self.assertTrue(percentage(self.cur, self.table, self.rowCount))
        l = percentage(self.cur, self.table, self.rowCount)
        self.assertTrue(abs(0.5-l[0][1]) <= abs(0.5-l[1][1]))

    def test_question(self):
        self.assertTrue(getQuestion(self.cur, self.table))
        self.assertTrue(getQuestion(self.cur, self.table)[0][0][0] == "I")

    def test_guess(self):
        self.assertEqual(guess_country(self.cur, self.table)['next_question_text'][0], "I", msg='{0}, {1}')
    
    def test_code_convert(self):
        self.assertEqual(get_country_name("AUS"), "Australia", msg='{0}, {1}')
        self.assertEqual(get_country_name("GBR"), "United Kingdom", msg='{0}, {1}')

    def test_get_country_list(self):
        self.assertEqual(len(get_all_country(self.cur, self.table)), self.rowCount, msg='{0}, {1}')
   
if __name__=='__main__':
    unittest.main(verbosity=2)