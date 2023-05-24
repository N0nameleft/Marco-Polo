import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create db for later use
db = SQLAlchemy()

def create_app():
    # set app and config
    app = Flask(__name__, static_folder='static')
    app.config["SECRET_KEY"] = "thisIsASampleKey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    # set login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # import user for current session
    from .models import User

    # load user info
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # auth routes blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # general routes blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
