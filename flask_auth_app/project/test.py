import sqlite3

def list_tables():
    conn = sqlite3.connect('countries.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    conn.close()
    return [table[0] for table in tables]

tables = list_tables()
print(tables)
