import sqlite3
from flask import g
import os
from datetime import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('countries.db')
    return g.db

def temp_game_db(userId):
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

    
    

    
    

    return g.temp


def add_temp(cur):
    return cur  

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()



# os.remove("zach.db")