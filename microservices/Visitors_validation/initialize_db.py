import sqlite3
con = sqlite3.connect('./microservices/Visitors_validation/database.db')

try:
    with con:
        con.execute('CREATE TABLE museums (id integer primary key, name text,position text, ip text)')
        con.execute('CREATE TABLE bookings (id text, date text,customer text,museum text,prize double )')
        con.execute('INSERT INTO museums (name,position,ip) VALUES ("Uffizi","Firenze","http://127.0.0.1:5010/")')
except sqlite3.Error:
    print("Error initializing database")

con.close()