import sqlite3
con = sqlite3.connect('database.db')

try:
    with con:
        con.execute('CREATE TABLE museums (id text, name text,position text, ip text)')
        con.execute('CREATE TABLE bookings (id text, date text,customer text,museum text,prize double )')
except sqlite3.Error:
    print("Error initializing database")

con.close()