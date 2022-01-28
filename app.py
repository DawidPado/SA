import hashlib
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


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)


@app.route('/signin/', methods=['POST'])
def singin():
    parser.add_argument("name")
    parser.add_argument("surname")
    parser.add_argument("username")
    parser.add_argument("email")
    parser.add_argument("password")
    args = parser.parse_args()
    h = hashlib.md5(args["password"].encode())
    password = h.hexdigest()
    query = "{\
   \"query\": {\
   \"bool\": {\
     \"must\": [\
       {\
         \"match\": {\
           \"email\": \"" + args["email"] + "\"\
         }\
       },\
       {\
         \"match\": {\
           \"username\": \"" + args["username"] + "\"\
         }\
       }\
     ]\
   }\
   }\
   }"
    # print(query)
    res = es.search(index='users', body=query)

    if res['hits']['hits'] == []:
        es.index(index='users',
                 document={'username': args["username"], 'name': args["name"], 'surname': args["surname"],
                           'email': args["email"], 'password': password})
        session["name"] = args["name"]
        session["surname"] = args["surname"]
        session['email'] = args["email"]
        session['username'] = args["username"]
        session['logged_in'] = True
        status = {"status": "created"}
        return status
    else:
        status = {"status": "username or email already in database"}
        return status


@app.route('/login/', methods=['POST'])
def login():
    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()
    h = hashlib.md5(args["password"].encode())
    password = h.hexdigest()
    query = "{\
\"query\": {\
\"bool\": {\
  \"must\": [\
    {\
      \"match\": {\
        \"password\": \"" + password + "\"\
      }\
    },\
    {\
      \"match\": {\
        \"username\": \"" + args["username"] + "\"\
      }\
    }\
  ]\
}\
}\
}"
    # return {"status":args["username"]}
    res = es.search(index='users', body=query)
    print(args, query, res)
    if res['hits']['hits'] != []:
        if res['hits']['hits'][0]['_source']["username"] == args["username"] and res['hits']['hits'][0]['_source'][
            "password"] == password:
            session["name"] = res['hits']['hits'][0]['_source']["name"]
            session["surname"] = res['hits']['hits'][0]['_source']["surname"]
            session['email'] = res['hits']['hits'][0]['_source']["email"]
            session['logged_in'] = True
            status = {"status": "success"}
            return status
        else:
            status = {"status": "wrong credential"}
            return status
    status = {"status": "fail"}
    return status


@app.route('/booking/', methods=['POST'])
def rings():
    if len(session) > 0:
        if session['logged_in'] == True:
            parser.add_argument("date")
            parser.add_argument("place")
            args = parser.parse_args()
            doc = {
                'email': session['email'],
                'name': session['name'],
                'surname': session['surname'],
                'place': args["place"],
                'date': args["date"],
            }
            x = es.index(index='bookings', document=doc)
            print(x)
            """dictToSend = {'question': 'what is the answer?'}
            res = requests.post('http://localhost:5001/qr_generator', json=dictToSend)
            print('response from server:', res.text)
            dictFromServer = res.json()"""

            return {"status": "done"}, 200
    return {"status": "not authorized"}


"""@app.route('/rings/', methods = ['POST'])
def rings():
    es.index(
        index='lord-of-the-rings',
        document={
            'character': 'Aragon',
            'quote': 'It is not this day.'
        })

    return {"status":"done"}"""
