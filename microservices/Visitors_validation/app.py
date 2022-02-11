import datetime
import sqlite3

import shortuuid
from flask import Flask, render_template, request, session
from flask_cors import CORS
from flask_restful import Api, reqparse
import requests

app = Flask(__name__)
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'
api = Api(app)
parser = reqparse.RequestParser()
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World! from ms2'


@app.route('/booking/', methods=['POST'])
def booking():
        parser.add_argument("date")
        parser.add_argument("museum")
        parser.add_argument("prize")
        parser.add_argument("customer")
        args = parser.parse_args()
        id = str(shortuuid.uuid())
        statment = "INSERT INTO bookings VALUES (?,?,?,?,?)"
        # (id text, date text,customer text,museum text,prize double )
        values = (id, args['date'], args['customer'], args['museum'], args['prize'])
        con = sqlite3.connect('database.db')
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y")
        # pr
        try:
            with con:
                if now==args['date']:
                    res = con.execute("SELECT ip FROM museums WHERE name=?",
                                      (args['museum']))
                    for ip in res:
                        dictToSend = {'id' : id}
                        res = requests.post('http://'+ip+'/reservations/add/', json=dictToSend) #sent to middleware second ms museo, data, e utente
                        dictFromServer = res.json()
                        if dictFromServer['success']==True:
                            con.execute(statment, values)
                            status={'status':'ok'},200
                        else:
                            status = {'status': 'internal server error'}, 500
                else:
                    con.execute(statment, values)
                    status = {'status': 'ok',
                              'code': id}, 200
        except sqlite3.Error:
            status = {'status': 'internal server error'}, 500
        con.close()
        return status

@app.route('/send_all/', methods=['POST'])
def send_bookings():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y")
    con = sqlite3.connect('database.db')
    museums=dict()
    try:
        with con:
            res = con.execute("SELECT * FROM museums")
            for record in res:
                museums[record[1]]=record[3] #row[1]==museum name #row[3]==mueum ip
            for museum in museums:
                res = con.execute("SELECT * FROM bookings where date=? and museum=?", (now,museum))
                ids=[]
                for record in res:
                    ids.append(record[0])
                dictToSend = {'ids': ids}
                res = requests.post('http://' + museums[museum] + '/reservations/update',
                                    json=dictToSend)
                dictFromServer = res.json()
                if dictFromServer['success'] == True:
                    status = {'status': 'ok'}, 200
                else:
                    status = {'status': 'internal server error'}, 500
                    break
    except sqlite3.Error:
        status = {'status': 'internal server error'}, 500
    con.close()
    return status

if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)