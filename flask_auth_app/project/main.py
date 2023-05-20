from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from .decisionMaking import guess_country, get_next_question
from .database import get_db  # Don't forget to import your database connection function

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

@main.route('/start_game', methods=['POST'])
def start_game():
    # Get the database connection
    conn = get_db()
    cur = conn.cursor()

    # Get all countries to start the game
    cur.execute("SELECT countrycode FROM completedata")
    all_countries = [row[0] for row in cur.fetchall()]

    # Save the initial game state in the user's session
    session['current_countries'] = all_countries

    # Close the cursor and database connection
    cur.close()
    conn.close()

    # Get the first question
    result = get_next_question(None, None)  # Passing only two arguments which match the function definition

    return jsonify(result)


@main.route('/get_question', methods=['POST'])
def get_question():
    data = request.get_json()
    user_response = data.get('user_response')
    prev_characteristic = data.get('prev_characteristic')

    # Retrieve the game state from the user's session
    current_countries = session.get('current_countries', [])

    result = get_next_question(user_response, prev_characteristic)

    if 'countries_left' in result and result['countries_left'] <= 5:
        countries_to_guess = result.get('countries_to_guess', [])
        for country in countries_to_guess:
            if guess_country(country):  # Here is where we call guess_country in your web app
                result['next_question_text'] = f"Your country is {country}!"
                break
        else:
            result['next_question_text'] = "I couldn't guess your country. Let's try again."

    # Save the updated game state in the user's session
    session['current_countries'] = result.get('countries', [])

    return jsonify(result)

