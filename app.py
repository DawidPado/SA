import hashlib

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

    con = sqlite3.connect('database.db')
    try:
        with con:
            exist = False
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
    except sqlite3.Error:
        status = {'status': 'internal server error'}, 500
    con.close()
    return status


@app.route('/login/', methods=['POST'])
def login():
    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()
    h = hashlib.md5(args["password"].encode())
    password = h.hexdigest()
    con = sqlite3.connect('database.db')
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
    print(session)
    if len(session) > 0:
        if session['logged_in'] == True:
            parser.add_argument("date")
            parser.add_argument("museum")
            args = parser.parse_args()
            id = str(shortuuid.uuid())
            prize=10.00
            statment = "INSERT INTO bookings VALUES (?,?,?,?,?)"
            # (id text, date text,customer text,museum text,prize double )
            values = (id, args['date'], session['email'], args['museum'], prize)
            con = sqlite3.connect('database.db')
            try:
                with con:
                    dictToSend = {'id' : id}
                    res = requests.post('http://someip:8080/', json=dictToSend) #sent to midleware
                    dictFromServer = res.json()
                    if dictFromServer['status']=='ok':
                        con.execute(statment, values)
                        status={'status':'ok'},200
                    else:
                        status = {'status': 'internal server error'}, 500
            except sqlite3.Error:
                status = {'status': 'internal server error'}, 500
            con.close()
            return status
    return {"status": "Unauthorized"},401


"""@app.route('/rings/', methods = ['POST'])
def rings():
    es.index(
        index='lord-of-the-rings',
        document={
            'character': 'Aragon',
            'quote': 'It is not this day.'
        })

    return {"status":"done"}"""
