import sqlite3
con = sqlite3.connect('./microservices/Users_service/database.db')

try:
    with con:
        con.execute('CREATE TABLE users (id text, name text,surname text,username text,email text,password text)')
        con.execute('CREATE TABLE schedules (id integer primary key, date text,museum text,prize double )')
        con.execute('INSERT INTO schedules (date, museum, prize) VALUES ("17/02/2022", "Uffizi",15.0)')
except sqlite3.Error:
    print("Error initializing database")

con.close()