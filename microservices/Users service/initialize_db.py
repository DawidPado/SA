import sqlite3
con = sqlite3.connect('database.db')

try:
    with con:
        con.execute('CREATE TABLE users (id text, name text,surname text,username text,email text,password text)')
        con.execute('CREATE TABLE museums (id text, name text,position text,schedule text)')
        con.execute('CREATE TABLE schedules (id text, date text,open text,close text,bookings integer )')
        con.execute('CREATE TABLE bookings (id text, date text,customer text,museum text,prize double )')
except sqlite3.Error:
    print("Error initializing database")

con.close()