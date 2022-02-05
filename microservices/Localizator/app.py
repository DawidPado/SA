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
def localizator():  # put application's code here
    parser.add_argument("id") #prenotation id/ id is unique so it can rappresent a visitor
    parser.add_argument("position")
    args = parser.parse_args()
