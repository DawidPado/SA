import sqlite3

con = sqlite3.connect('./microservices/Localizator/database.db')

try:
    with con:
        con.execute('CREATE TABLE IPs (id text, name text, ip text)') #where to send data
        con.execute('CREATE TABLE positions (id integer primary key, museum text, x integer, y integer, z integer, booking_id text)')
        
except sqlite3.Error as er:
        error="Insert into near_artworks went wrong: " + ' '.join(er.args)
        print(error)