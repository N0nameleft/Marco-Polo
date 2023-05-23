import sqlite3
from flask import g
import os
from .decisionMaking import *


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('countries.db')
        # Create the user_responses table if it doesn't exist
        create_responses_db()
    return g.db


def create_responses_db():
    # Connect to the database
    conn = get_db()
    cur = conn.cursor()

    # Create the user_responses table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id INTEGER,
            question TEXT,
            response TEXT
        )
    """)

    # Commit changes and close connection
    conn.commit()
    cur.close()


def insert_response(user_id, session_id, question, response):
    # Connect to the database
    conn = get_db()
    cur = conn.cursor()

    # Insert the user's response into the user_responses table
    cur.execute("""
        INSERT INTO user_responses (user_id, session_id, question, response)
        VALUES (?, ?, ?, ?)
    """, (user_id, session_id, question, response))

    # Commit changes and close connection
    conn.commit()
    cur.close()


def new_game_db(user_id):
    name = '%s.db' % user_id
    g.temp = sqlite3.connect(name)

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
    name = '%s.db' % user_id
    g.temp = sqlite3.connect(name)
    return g.temp


def add_temp(cur):
    return cur  


def update_game_db(conn, table, user_response, prev_characteristic):
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

    conn.commit()
    

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
