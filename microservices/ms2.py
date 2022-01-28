import datetime

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
    app.run(host="localhost", port=8000, debug=True)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World! from ms2'


@app.route('/checkin', methods = ['POST'])
def checkin():

    # qr code will be generated on client side by booking id
    # qr code è una rappresentazione grafica del id quidni nessun problema su dove è generato

    parser.add_argument("id")
    args = parser.parse_args()
    query = {
        "query": {
            "term": {
                "_id": args["id"]
            }
        }
    }
    res = es.search(index='bookings',body=query)
    if res['hits']['hits'] != []:
        date = res['hits']['hits'][0]['_source']["date"]
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y")
        if date==now:
            ##################
            # todo
            ##################
            return {"status":"qr code valid"},200
        else:
            return {"status": "qr code not valid"}, 422
    else:
        return {"status": "qr not found"}, 404

@app.route('/checkout', methods = ['POST'])
def checkout():
    parser.add_argument("id")
    args = parser.parse_args()
    query = {
        "query": {
            "term": {
                "_id": args["id"]
            }
        }
    }
    res = es.search(index='bookings', body=query)
    if res['hits']['hits'] != []:
        date = res['hits']['hits'][0]['_source']["date"]
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y")
        if date == now:
            ##################
            #todo
            ##################
            return {"status": "qr code valid"}, 200
        else:
            return {"status": "qr code not valid"}, 422
    else:
        return {"status": "qr not found"}, 404


