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
print(__name__)

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
        print(date)
        return {"status":"qr code valid"},200
    else:
        return {"status": "qr not found"}, 404

@app.route('/read_qr', methods = ['POST'])
def checkout():
    parser.add_argument("id")

    es.index(
        index='lord-of-the-rings',
        document={
            'character': 'Aragon',
            'quote': 'It is not this day.'
        })

    return {"status":"done"}


