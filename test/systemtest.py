import unittest, os
from app import create_app, db
from app.models import User
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
class AccessTest(unittest.TestCase):
    driver = None
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, "geckodriver"))
        if not self.driver:
            self.skipTest("Web browser is not available")
        else:
            self.app = create_app
            db.init_app(self.app)
            db.create_all()
            u1 = User(id=1011, username="Test11", email="test11@mail.com")
            u1.password(generate_password_hash("test11"))
            db.session.add(u1)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get("http://127.0.0.1:5000/")
    
    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        user = User.query.get(1011)
        self.assertEqual(user.username, "Test11", msg="no such user")

        self.driver.get("http://127.0.0.1:5000/signup")
        self.driver.implicitly_wait(5)

        username_field = self.driver.find_element_by_name("email")
        username_field.send_keys("test12@mail.com")
        email_field = self.driver.find_element_by_name("username")
        email_field.send_keys("Test12")
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("test12")
        register = self.driver.find_element_by_id("sign_up")
        register.click()
        self.driver.implicitly_wait(5)

        self.driver.find_element_by_xpath("//option[text()='Login']").click()
        username_field = self.driver.find_element_by_name("email")
        username_field.send_keys("test12@mail.com")
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("test12")
        login = self.driver.find_element_by_id("log_in")
        login.click()
        self.driver.implicitly_wait(5)

        self.driver.find_element_by_xpath("//option[text()='Logout']").click()

    def test_login_logout(self):
        user = User.query.get(1011)
        self.driver.get("http://127.0.0.1:5000/login")
        self.driver.implicitly_wait(5)

        username_field = self.driver.find_element_by_name("email")
        username_field.send_keys(user.email)
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("test11")
        login = self.driver.find_element_by_id("log_in")
        login.click()
        self.driver.implicitly_wait(5)

        self.driver.find_element_by_xpath("//option[text()='Logout']").click()


class GameTest(unittest.TestCase):
    driver = None
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, "geckodriver"))
        self.app = create_app
        db.init_app(self.app)
        db.create_all()

        u1 = User(id=1011, username="Test11", email="test11@mail.com")
        u1.password(generate_password_hash("test11"))
        db.session.add(u1)
        db.session.commit()
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.find_element_by_xpath("//option[text()='Login']").click()

        username_field = self.driver.find_element_by_name("email")
        username_field.send_keys(user.email)
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("test11")
        self.driver.find_element_by_id("log_in").click()
        self.driver.implicitly_wait(5)

    
    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.remove()
            db.drop_all()
    
    def test_profile_and_history(self):
        self.driver.find_element_by_xpath("//option[text()='Profile']").click()
        self.driver.find_element_by_id("start_button").click()
        self.driver.find_element_by_xpath("//option[text()='History']").click()
        self.driver.find_element_by_id("start_button").click()
    
    def test_start_game(self):
        self.driver.find_element_by_xpath("//option[text()='Home']").click()
        self.driver.find_element_by_id("start-button").click()
        self.driver.find_element_by_id("yes").click()
        self.driver.find_element_by_id("yes").click()
        self.driver.find_element_by_id("yes").click()
        self.driver.find_element_by_xpath("//option[text()='History']").click()
        History = self.driver.find_element_by_xpath("//option[text()='Game Attempt']")
        self.assertTrue(History)


if __name__ == "__main__":
    unittest.main(verbosity=2)