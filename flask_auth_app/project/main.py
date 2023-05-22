from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from .decisionMaking import *
from .database import *  # Don't forget to import your database connection function
import sqlite3

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

@main.route("/game")
def new_page():
    return render_template("game.html")

@main.route('/start_game', methods=['POST'])
def start_game():
    # Get the database connection
    conn = get_db()
    cur = conn.cursor()
# tempconn = temp_game_db(current_user.id)
#     tempcur = tempconn.cursor()
#     add_temp(tempcur)
    temp = temp_game_db(current_user.id)
    # Get all countries to start the game
    table = 'completedata'
    cur.execute("SELECT countrycode FROM %s" % table)
    all_countries = [row[0] for row in cur.fetchall()]

    # Save the initial game state in the user's session
    session['current_countries'] = all_countries

    # Get the first question
    result = get_next_question(cur, table)

    # Close the cursor and database connection
    cur.close()
    conn.close()
    temp.close()

    return jsonify(result)


@main.route('/get_question', methods=['POST'])
def get_question():
    data = request.get_json()
    user_response = data.get('user_response')
    prev_characteristic = data.get('prev_characteristic')

    # test
    conn = get_db()
    cur = conn.cursor()

    # Retrieve the game state from the user's session
    current_countries = session.get('current_countries', [])

    # temp
    table = 'completedata'

    result = get_next_question(cur, table,user_response, prev_characteristic)

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

    # test
    cur.close()
    conn.close()

    return jsonify(result)

