import hashlib
import sqlite3
import  uuid

terms=[]
terms.append('5')
terms.append('Dawid')
terms.append('Pado')
terms.append('Dawid')
terms.append('prova@gmail.com')
terms.append(hashlib.md5('password'.encode()).hexdigest())
values=(terms[0],terms[1],terms[2],terms[3],terms[4],terms[5])
statment="INSERT INTO USERS VALUES (?,?,?,?,?,?)"

print(uuid.uuid4())
con = sqlite3.connect('users.db')
try:
    with con:
        # delete all old reservations
        #res = con.execute(statment,values)
        # parse and insert new reservations
        res = con.execute("SELECT * FROM USERS WHERE username=? or email=?",('Dawid','Ciao'))
# SQL exception handler
except sqlite3.Error:
    print('dont work')
for record in res:
    print(record[0])
con.close()
