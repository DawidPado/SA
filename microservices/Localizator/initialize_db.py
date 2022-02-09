import sqlite3

con = sqlite3.connect('database.db')

try:
    with con:
        con.execute('CREATE TABLE IPs (id text, name text, ip text)') #where to send data
        con.execute('CREATE TABLE position (id text, museum text, position text, booking_id text)')
        
except sqlite3.Error:
    print("Error initializing database")

con.close()