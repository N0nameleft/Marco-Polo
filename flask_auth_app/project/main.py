from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from .decisionMaking import *
from .database import *
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
    # conn = get_db()
    # cur = conn.cursor()
#   tempconn = temp_game_db(current_user.id)
#   tempcur = tempconn.cursor()
#   add_temp(tempcur)

    temp, table = new_game_db(current_user.id)
    tempcur = temp.cursor()

    # cur.close()
    # conn.close()

    # Get all countries to start the game
    tempcur.execute("SELECT countrycode FROM %s" % table)
    all_countries = [row[0] for row in tempcur.fetchall()]

    countQuery = "SELECT COUNT(*) FROM %s" % table
    tempcur.execute(countQuery)
    rowCount = tempcur.fetchone()[0]
    # Save the initial game state in the user's session
    session['countries_count'] = rowCount
    session['current_countries'] = all_countries

    # Get the first question
    result = get_next_question(tempcur, table)
    

    # Close the cursor and database connection
    tempcur.close()
    temp.close()

    return jsonify(result)


@main.route('/get_question', methods=['POST'])
def get_question():
    data = request.get_json()
    user_response = data.get('user_response')
    prev_characteristic = data.get('prev_characteristic')
    conn = get_game_db(current_user.id)
    cur = conn.cursor()
    t  = "tem"
    update_game_db(conn, t, user_response, prev_characteristic)

    # Retrieve the game state from the user's session
    # current_countries = session.get('current_countries', [])
    countries_count = session.get('countries_count')
    if countries_count <=5:
    # if 'countries_left' in result and result['countries_left'] <= 3:
        # if result['countries_left'] == 1:
        #     guess_country(cur, table)
        # # countries_to_guess = result.get('countries_to_guess', [])
        # else:
        f_r = guess_country(cur, t)
        session['countries_count'] = f_r.get('countries_left')
        session['current_countries'] = f_r.get('countries', [])
        return jsonify(f_r)



        # for i in range(result["countries_left"]):
        #     if guess_country(cur, t):  # Here is where we call guess_country in your web app
        #         result['next_question_text'] = f"Your country is {country}!"
        #         break
        # else:
        #     result['next_question_text'] = "I couldn't guess your country. Let's try again."
    else:
        result = get_next_question(cur, t, user_response, prev_characteristic)
    # Save the updated game state in the user's session
        session['countries_count'] = result.get('countries_left')
        session['current_countries'] = result.get('countries', [])

    # test
    cur.close()
    conn.close()

    return jsonify(result)

# This is the function to render game logs in game_session.html
# @main.route("/game_session/<session_id>")
# @login_required
# def game_session(session_id):
#     # # Get the database connection
#     # conn = get_db()
#     # cur = conn.cursor()

#     # # Query the database for the game session with the provided id
#     # cur.execute("SELECT * FROM game_sessions WHERE session_id = ?", (session_id,))

#     # # Fetch the results
#     # game_session_data = cur.fetchall()

#     # # Close the cursor and database connection
#     # cur.close()
#     # conn.close()

#     # Render the game_session template with the game session data
#     return render_template("game_session.html") #game_session_data=game_session_data)
@main.route("/game_session/<session_id>")
def game_session(session_id):
    return render_template("game_session.html", session_id=session_id)
