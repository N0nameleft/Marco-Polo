import sqlite3
from flask import g
import os
from .decisionMaking import *
from datetime import datetime


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('countries.db')
    return g.db

def new_game_db(user_id):
    name = '%s_temp.db' % user_id
    if os.path.exists(name):
        os.remove(name)
    g.temp = sqlite3.connect(name)
    get_history_db(user_id)
    tcur = g.temp.cursor()
    table = "tem"
    tcur.execute("DROP TABLE IF EXISTS %s" % table)
    # Attach the original database to the user's database
    tcur.execute("ATTACH DATABASE 'countries.db' AS origin_db")

    # Create a new table in the user's database with the same structure as completedata
    tcur.execute(f"CREATE TABLE {table} AS SELECT * FROM origin_db.completedata")
    
    g.temp.commit()

    # Detach the original database
    tcur.execute("DETACH DATABASE origin_db")
    
    return g.temp, table

def get_game_db(user_id):
    name = '%s_temp.db' % user_id
    g.temp = sqlite3.connect(name)
    return g.temp


def add_temp(cur):
    return cur  

def update_game_db(conn, table, user_response, prev_characteristic, user_id):
    cur = conn.cursor()
    if user_response == "yes":
        q = "DELETE FROM %s WHERE %s = 0" % (table, prev_characteristic)
    else:  # handle 'no' response
        q = "DELETE FROM %s WHERE %s = 1" % (table, prev_characteristic)

    cur.execute(q)

    # delete columns with all same value
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



def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()



def write_chat_result(userId, user_response, question):
    name = '%s.db' % userId
    conn = sqlite3.connect('instance/history/%s' %name)
    cur = conn.cursor()
    q_name = "SELECT time FROM game_result ORDER BY id DESC LIMIT 1"
    cur.execute(q_name)
    table = "%s" % cur.fetchone()[0]
    if user_response == "yes":
        result = "Bot successed"
    else:
        result = "Bot failed"
    c1 = question.replace("Are you in ", "")
    country = c1.replace("?", "")
    q= "UPDATE game_result SET (result, guessing_country) =('%s', '%s') WHERE time = %s " %(result, country, table)
    cur.execute(q)
    conn.commit()
    cur.close()
    conn.close()
