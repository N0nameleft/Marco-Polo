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
    temp, table = new_game_db(current_user.id)
    tempcur = temp.cursor()
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
    current_question = data.get('current_question')
    userId = current_user.id
    conn = get_game_db(userId)
    cur = conn.cursor()
    t  = "tem"
    
    if "Are you" in current_question:
        result = game_finish(user_response)
        write_chat_result(userId, user_response, current_question)
        return jsonify(result)
   

    update_game_db(conn, t, user_response, prev_characteristic, current_user.id)

    # Retrieve the game state from the user's session
    cur.execute("SELECT COUNT(*) FROM %s" % t)
    countries_count = cur.fetchone()[0]
    columnLeft = len(getColumnNames(cur, t))

    if countries_count <=5 or columnLeft == 0:
        f_r = guess_country(cur, t)
        session['countries_count'] = f_r.get('countries_left')
        session['current_countries'] = f_r.get('countries', [])
        return jsonify(f_r)

    else:
        result = get_next_question(cur, t)
        session['countries_count'] = result.get('countries_left')
        session['current_countries'] = result.get('countries', [])

    # test
    cur.close()
    conn.close()

    return jsonify(result)

@main.route('/game_session/<session_id>')
def game_session(session_id):
    
    conn = sqlite3.connect('instance/history/%s.db' % current_user.id)
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM game{session_id}")
        data = cursor.fetchall()
        chat_entries = [{'question': 'Is your country ' + row[1].replace('_', ' ') + '?', 'answer': row[2].capitalize()} for row in data]
        return render_template('game_session.html', chat_entries=chat_entries)

    except sqlite3.Error as e:
        print("An error occurred:", e)

    finally:
        conn.close()

    return "Error: Game session not found"



@main.route("/history")
@login_required
def history():
    conn = sqlite3.connect('instance/history/{}.db'.format(current_user.id))
    cur = conn.cursor()
    new_table = "CREATE TABLE IF NOT EXISTS game_result (id INTEGER PRIMARY KEY, time INTEGER, result INTEGER)"
    cur.execute(new_table)
    conn.commit()
    cur.execute("SELECT * FROM game_result")
    r = cur.fetchall()
    attempts = [ [i[1], format_time(i[1]), i[2], i[3].capitalize()if i[3] is not None else "Incomplete"] for i in reversed(r)]

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

@main.route("/new_game")
def new_game():
    # Code to start a new game
    return render_template("game.html")

