from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .decisionMaking import guess_country, get_next_question

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.username)

@main.route("/history")
@login_required
def history():
    return render_template("history.html")

@main.route("/question")
def new_page():
    return render_template("question.html")


@main.route('/get_question', methods=['POST'])
def get_question():
    data = request.get_json()
    user_response = data.get('user_response')
    prev_characteristic = data.get('prev_characteristic')

    result = get_next_question(user_response, prev_characteristic)

    if 'countries_left' in result:
        countries_left = result['countries_left']
        if countries_left <= 5:
            for country in result['countries']:
                if guess_country(country):  # Here is where we call guess_country in your web app
                    result['next_question_text'] = f"Your country is {country}!"
                    break
            else:
                result['next_question_text'] = "I couldn't guess your country. Let's try again."

    return jsonify(result)
