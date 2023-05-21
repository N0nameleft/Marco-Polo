import sqlite3
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('countries.db')
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()