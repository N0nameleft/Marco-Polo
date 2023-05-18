import sqlite3

def percentage():
    con = sqlite3.connect(countries.db)
    con.cursor = ("SELECT * from completedData")
    
    