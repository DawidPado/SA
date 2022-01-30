import sqlite3

con = sqlite3.connect('reservations.db')

try:
    with con:
        con.execute('CREATE TABLE reservations (id text, checkin integer)')
        
except sqlite3.Error:
    print("Error initializing database")

con.close()