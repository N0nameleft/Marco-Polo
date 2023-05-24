from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint("auth", __name__)

# login page
@auth.route("/login")
def login():
    return render_template("login.html")

# after login
@auth.route("/login", methods=["POST"])
def login_post():
    # grab detail entered
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    # validate email, if doesn exist flask message
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Email or password is not correct, please try again.")
        return redirect(url_for("auth.login"))
    
    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))

# signup page
@auth.route("/signup")
def signup():
    return render_template("signup.html")

# after signup
@auth.route("/signup", methods=["POST"])
def signup_post():
    # grab detail entered
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    # validate email, if already exist flask message, ask user to login
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists.")
        return redirect(url_for("auth.signup"))
    
    # create new user if pass validation
    new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

# logout page
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html")

