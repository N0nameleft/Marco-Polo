import sqlite3
from flask import g
import os
from datetime import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('countries.db')
    return g.db
time = ""
def new_game_db(userId):
    name = '%s.db' % userId
    g.temp = sqlite3.connect(name)

    tcur = g.temp.cursor()
    
    origin = get_db()
    cur = origin.cursor()
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='completedata'")
    
    now = datetime.now()
    time = now.strftime("User%d%m%Y%H%M%S")
    q = cur.fetchone()[0]
    query = q.replace("completedata", time)
    tcur.execute(query)
    
    g.temp.close()
    g.temp = sqlite3.connect(name)
    cur.execute("ATTACH DATABASE '%s' AS destination" % name)
    cur.execute("INSERT INTO destination.%s SELECT * FROM completedata" % time)
    g.temp.commit()
    # cur.execute("DETACH destination")
    
    return g.temp, time

def get_game_db(userId):
    name = '%s.db' % userId
    g.temp = sqlite3.connect(name)
    return g.temp

def get_table_name():
    return time

def add_temp(cur):
    return cur  

def update_game_db(cur, table, user_response, prev_characteristic):
    q = "DELETE FROM %s WHERE " %table

    if user_response == "yes":
        where_clause += " AND %s = 0" %prev_characteristic
    else:  # handle 'no' response
        where_clause += " AND %s = 1" %prev_characteristic

    cur.execute(q)
    



def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()



# os.remove("zach.db")