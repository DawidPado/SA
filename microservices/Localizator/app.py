import datetime
import sqlite3

from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, session
from flask_cors import CORS
from flask_restful import Api, reqparse
import requests

app = Flask(__name__)
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'
api = Api(app)
parser = reqparse.RequestParser()
CORS(app)
es = Elasticsearch()

if __name__ == '__main__':
    app.run(host="localhost", port=5002, debug=True)

@app.route('/position/update')
def localizator():  # put application's code here
    parser.add_argument("id") #prenotation id/ id is unique so it can rappresent a visitor
    parser.add_argument("position")
    args = parser.parse_args()
    con = sqlite3.connect('database.db')
    try:
        with con:
            exist = False
            res = con.execute("SELECT ip FROM IPs")
            for ip in res:
                dictToSend = {'id': args['id'],
                              'position': args['position'],
                              }
                requests.post(ip+'/crowd', json=dictToSend)  # sent to middleware

    except sqlite3.Error:
        status = {'status': 'internal server error'}, 500
    con.close()
    return status
