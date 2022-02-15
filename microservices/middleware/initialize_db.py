import sqlite3
import random
import string

con = sqlite3.connect('./microservices/middleware/reservations.db')

try:
    with con:
        con.execute('CREATE TABLE IF NOT EXISTS reservations (id text, checkin integer)')
        i = 0
        while i<500:
            id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            con.execute("INSERT INTO reservations (id, checkin) VALUES (?, 1)",[id])
            i+=1
        
except sqlite3.Error as er:
        error="Insert into reservations went wrong: " + ' '.join(er.args)
        print(error)
        print()

con.close()