import sqlite3

con = sqlite3.connect('reservations.db')

try:
    with con:
        con.execute('CREATE TABLE IPs (name text, ip text)') #where to send data
        con.execute('CREATE TABLE position (museum text, position text, booking_id text)')
        
except sqlite3.Error:
    print("Error initializing database")

con.close()