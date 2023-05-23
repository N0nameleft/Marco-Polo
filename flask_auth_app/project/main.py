from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from .decisionMaking import *
from .database import *
import sqlite3
from .database import get_game_db
main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.username)


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
    update_game_db(conn, t, user_response, prev_characteristic, current_user.id)

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
        result = get_next_question(cur, t)
    # Save the updated game state in the user's session
        session['countries_count'] = result.get('countries_left')
        session['current_countries'] = result.get('countries', [])

    # test
    cur.close()
    conn.close()

    return jsonify(result)

# Python code in Flask route


@main.route('/game_session/<session_id>')
def game_session(session_id):
    # Connect to the user_id.db database
    
    conn = sqlite3.connect('%s.db' % current_user.id)
    print('%s.db' % current_user.id)
    cursor = conn.cursor()

    try:
        # Retrieve data from the specified table
        cursor.execute(f"SELECT * FROM game{session_id}")
        data = cursor.fetchall()

        # Prepare chat_entries based on the retrieved data
        chat_entries = [{'question': row[0], 'answer': row[1]} for row in data]

        # Render the game_session.html template and pass the chat_entries
        return render_template('game_session.html', chat_entries=chat_entries)

    except sqlite3.Error as e:
        # Handle any errors that may occur
        print("An error occurred:", e)

    finally:
        # Close the database connection
        conn.close()

    # Add a fallback
    return "Error: Game session not found"



@main.route("/history")
@login_required
def history():
    # Get the database connection
    conn = sqlite3.connect('instance/history/{}.db'.format(current_user.id))
    cur = conn.cursor()

    # Retrieve all attempts for the logged-in user
    cur.execute("SELECT * FROM game_result")
    attempts = cur.fetchall()

    # Close the cursor and database connection
    cur.close()
    conn.close()

    return render_template("history.html", attempts=attempts)

@main.route("/get_attempts")
@login_required
def get_attempts():
    # Get the database connection
    conn = sqlite3.connect('instance/history/{}.db'.format(current_user.id))
    cur = conn.cursor()

    # Retrieve all attempts for the logged-in user
    cur.execute("SELECT * FROM game_result")
    attempts = cur.fetchall()

    # Close the cursor and database connection
    cur.close()
    conn.close()

    return jsonify(attempts)
