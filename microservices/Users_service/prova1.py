import datetime
import hashlib
import sys
import traceback

import requests
from elasticsearch import Elasticsearch
from flask import Flask, session
from flask_cors import CORS
from flask_restful import Api, reqparse
import sqlite3
import shortuuid

app = Flask(__name__)
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'
api = Api(app)
parser = reqparse.RequestParser()
CORS(app)
es = Elasticsearch()
print(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/registration/', methods=['POST'])
def singin():
    parser.add_argument("name")
    parser.add_argument("surname")
    parser.add_argument("username")
    parser.add_argument("email")
    parser.add_argument("password")
    args = parser.parse_args()
    h = hashlib.md5(args["password"].encode())
    password = h.hexdigest()
    id = str(shortuuid.uuid())

    statment = "INSERT INTO USERS VALUES (?,?,?,?,?,?)"
    values = (id, args['name'], args['surname'], args['username'], args['email'], password)

    con = sqlite3.connect('../Users service/database.db')
    try:
        with con:
            exist = False
            res = con.execute("SELECT * FROM USERS WHERE username=? or email=?", ('Dawid', 'Ciao'))
            for record in res:
                print(record[0])

            res = con.execute("SELECT * FROM USERS WHERE username=? or email=?", (args['username'], args['email']))
            for result in res:
                exist = True
                break
            if not exist:
                con.execute(statment, values)
                session["name"] = args["name"]
                session["surname"] = args["surname"]
                session['email'] = args["email"]
                session['username'] = args["username"]
                session['logged_in'] = True
                status = {"status": "created"}, 200
            else:
                status = {"status": "username or email already in database"}, 300
            # parse and insert new reservations
    # SQL exception handler
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
        status = {'status': 'db internal server error'}, 500
    con.close()
    return status


@app.route('/login/', methods=['POST'])
def login():
    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()
    h = hashlib.md5(args["password"].encode())
    password = h.hexdigest()
    con = sqlite3.connect('../Users service/database.db')
    try:
        with con:
            res = con.execute("SELECT * FROM USERS WHERE username=? and password=?", (args['username'], password))
            found = False
            for result in res:
                session["name"] = result[1]
                session["surname"] = result[2]
                session['email'] = result[4]
                session['username'] = result[3]
                session['logged_in'] = True
                status = {"status": "logged"}, 200
                found = True
            if not found:
                status = {"status": "wrong username or password"}, 404
            # parse and insert new reservations
    # SQL exception handler
    except sqlite3.Error:
        status = {'status': 'internal server error'}, 500
    con.close()
    return status


@app.route('/booking/', methods=['POST'])
def booking():
    if len(session) > 0:
        if session['logged_in'] == True:
            parser.add_argument("date")
            parser.add_argument("museum")
            parser.add_argument("payment")
            parser.add_argument("prize")
            args = parser.parse_args()
            values = (args['date'], args['prize'], args['museum'])
            statment = "SELECT * FROM schedules WHERE date=? and prize=? and museum=?"
            con = sqlite3.connect('../Users service/database.db')
            found = False
            error=False
            status={}
            try:
                with con:
                    res = con.execute(statment,values)
                    for result in res:
                        found = True
                        break
            except sqlite3.Error:
                error=True
                status = {'status': 'internal server error'}, 500
            con.close()
            if error:
                return status
            if not found:
                return {'status': 'schedule not found'}, 404
            if check_payment(args["payment"]):
                dictToSend={"date":args['date'],
                            "museum":args['museum'],
                            "prize":args["prize"],
                            "customer":session['customre']}
                res = requests.post('http://localhost:5001/', json=dictToSend)
                dictFromServer = res.json()
                if dictFromServer['status']=='ok':
                    status={'status':'ok',
                            'code':dictFromServer['code']},200
                    make_payment(args["payment"])
                else:
                    status = {'status': 'internal server error'}, 500
                return status
            else:
                return {'status':'Bad request'},400
        return {"status": "Unauthorized"},401


def check_payment(data):
    #------
    #some code
    checked = True
    #------
    return checked
def make_payment(data):
    #------
    #some code
    done = True
    #------
    return done

#todo primo riceverre dati, check pagamento, mandare al 2 servizio e attendere il codice prenotazione da restituire al utente, ms 1 lista museo con orari e prezzi, e date

#todo 2ms riceve richiesta dal primo per prenotarlo, chech giorno se corrisponde al corrente scrive al middlewere e salva comunque, salva nel tutte le info della prenotazione,
# se non e giorno corrente non lo manda al middlewere.

#todo ms2 endopoit manda tutto di questo giorno che verra richiesto da uno script.