import sqlite3
from flask import g
import os


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('countries.db')
    return g.db

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




# def get_table_name():
#     return time

def add_temp(cur):
    return cur  

def update_game_db(conn, table, user_response, prev_characteristic):
    cur = conn.cursor()
    if user_response == "yes":
        q = "DELETE FROM %s WHERE %s = 0" % (table, prev_characteristic)

    else:  # handle 'no' response
        q = "DELETE FROM %s WHERE %s = 1" % (table, prev_characteristic)
    cur.execute(q)
    conn.commit()
    
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
