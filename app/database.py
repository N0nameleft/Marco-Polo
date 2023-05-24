# this is the file contain all the function related to 
# create/connect/update game database
# including countries which has all data, temporary database for current game
# chat history to store all question, answer, and final result
import sqlite3
from flask import g
import os
from .decisionMaking import *
from datetime import datetime

# get preset db, contains all data of countries
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('./data/countries.db')
    return g.db

# create a temporary db of this game for algo to access
def new_game_db(user_id):
    name = './data/%s_temp.db' % user_id
    # if exist old one, delete
    if os.path.exists(name):
        os.remove(name)
    # connect to db, if doesnt exist, will create one
    g.temp = sqlite3.connect(name)
    # create/connect history database, create table for this session
    get_history_db(user_id)

    # second check, if exist table, delete
    tcur = g.temp.cursor()
    table = "tem"
    tcur.execute("DROP TABLE IF EXISTS %s" % table)
    # Attach the original database to the temp database
    tcur.execute("ATTACH DATABASE './data/countries.db' AS origin_db")

    # Create a new table in the temp database with the same structure as completedata
    tcur.execute(f"CREATE TABLE {table} AS SELECT * FROM origin_db.completedata")
    
    g.temp.commit()

    # Detach the original database
    tcur.execute("DETACH DATABASE origin_db")
    
    return g.temp, table

def get_game_db(user_id):
    name = './data/%s_temp.db' % user_id
    g.temp = sqlite3.connect(name)
    return g.temp

# delete column and rows based on previous question, and user answer, to narrow down the data in table
# for easier algo process, and avoid asking the same question
def update_game_db(conn, table, user_response, prev_characteristic, user_id):
    cur = conn.cursor()

    # delete row where doesnt match prev answer
    if user_response == "yes":
        q = "DELETE FROM %s WHERE %s = 0" % (table, prev_characteristic)
    else:  # handle 'no' response
        q = "DELETE FROM %s WHERE %s = 1" % (table, prev_characteristic)

    cur.execute(q)

    # delete columns with all same value, as theres no point asking those
    columnNames = getColumnNames(cur, table)
    for c in columnNames:
        query = "SELECT COUNT( distinct %s) FROM %s" % (c, table)
        cur.execute(query)
        count = cur.fetchone()[0]
        if count == 1:
            q = "ALTER TABLE %s DROP COLUMN %s" % (table, c)
            cur.execute(q)
            conn.commit()
    update_chat_db(user_id, user_response, prev_characteristic)
    conn.commit()

# create/connect history database named as user_id.db, create result table if doesnt exist
# create table for the current game, to store chat history, for history function access to display chat history
def get_history_db(user_id):
    name = '%s.db' % user_id
    conn = sqlite3.connect('instance/history/%s' %name)
    cur = conn.cursor()
    new_table = "CREATE TABLE IF NOT EXISTS game_result (id INTEGER PRIMARY KEY, time INTEGER, guessing_country TEXT, result TEXT)"
    cur.execute(new_table)
    now = datetime.now()
    time = now.strftime("%Y%m%d%H%M%S")
    time_input = "INSERT INTO game_result(time) VALUES (%s)" % time
    cur.execute(time_input)
    new_chat = "CREATE TABLE game%s (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)" %time
    cur.execute(new_chat)
    conn.commit()
    cur.close()
    conn.close()

# write question and user answer into the current game table
def update_chat_db(user_id, answer, question):
    name = '%s.db' % user_id
    conn = sqlite3.connect('instance/history/%s' %name)
    cur = conn.cursor()
    q_name = "SELECT time FROM game_result ORDER BY id DESC LIMIT 1"
    cur.execute(q_name)
    table = "game%s" % cur.fetchone()[0]
    q1 = "INSERT INTO %s(question, answer) VALUES ('%s', '%s')" % (table,question,answer)
    cur.execute(q1)
    conn.commit()
    cur.close()
    conn.close()

# write in the last question asked, which is the country our program think it may be
# and write in user answer for whether its that country or not
# if it is the the program succeeded, else failed
def write_chat_result(userId, user_response, question):
    name = '%s.db' % userId
    conn = sqlite3.connect('instance/history/%s' %name)
    cur = conn.cursor()
    q_name = "SELECT time FROM game_result ORDER BY id DESC LIMIT 1"
    cur.execute(q_name)
    table = "%s" % cur.fetchone()[0]
    if user_response == "yes":
        result = "Bot succeeded"
    else:
        result = "Bot failed"
    c1 = question.replace("Are you in ", "")
    country = c1.replace("?", "")
    q= "UPDATE game_result SET (result, guessing_country) =('%s', '%s') WHERE time = %s " %(result, country, table)
    cur.execute(q)
    conn.commit()
    cur.close()
    conn.close()
