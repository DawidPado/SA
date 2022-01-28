import hashlib
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, session
from flask_cors import CORS
from flask_restful import Api, reqparse


app = Flask(__name__)
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'
api = Api(app)
parser = reqparse.RequestParser()
CORS(app)
es = Elasticsearch()

"""@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()"""


@app.route('/signin/', methods = ['POST'])
def singin():
   parser.add_argument("username")
   parser.add_argument("email")
   parser.add_argument("password")
   args = parser.parse_args()
   h = hashlib.md5(args["password"].encode())
   password=h.hexdigest()
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
   res = es.search(index='users', body=query)
   print(res)

   if res['hits']['hits'] == []:
       """data = {'ad_id': 1053674,
               'city': 'Houston',
               'category': 'Cars',
               'date_posted': datetime.datetime(2021, 1, 29, 19, 33),
               'title': '2020 Chevrolet Silverado',
               'body': "This brand new vehicle is the perfect truck for you.",
               'phone': None}"""
       es.index(index='users', document={ 'username':  args["username"] , 'email':  args["email"], 'password': password })
       session['username'] = args["username"]
       session['logged_in'] = True
       status = {"status": "created"}
       return status
   else:
       status = {"status": "username or email already in database"}
       return status




@app.route('/login/', methods = ['POST'])
def login():
   parser.add_argument("username")
   parser.add_argument("password")
   args = parser.parse_args()
   h = hashlib.md5(args["password"].encode())
   password=h.hexdigest()
   query="{\
\"query\": {\
\"bool\": {\
  \"must\": [\
    {\
      \"match\": {\
        \"password\": \"" + password +"\"\
      }\
    },\
    {\
      \"match\": {\
        \"username\": \""+args["username"]+"\"\
      }\
    }\
  ]\
}\
}\
}"
   #return {"status":args["username"]}
   res = es.search(index='users', body=query)
   print(args ,query , res)
   if res['hits']['hits'] != []:
       if res['hits']['hits'][0]['_source']["username"]==args["username"] and res['hits']['hits'][0]['_source']["password"]==password:
           session['username'] = args["username"]
           session['logged_in'] = True
           status = {"status": "success"}
           return status
       else:
           status = {"status": "wrong credential"}
           return status
   status = {"status": "fail"}
   return status

@app.route('/rings/', methods = ['POST'])
def rings():
    es.index(
        index='lord-of-the-rings',
        document={
            'character': 'Aragon',
            'quote': 'It is not this day.'
        })

    return {"status":"done"}

"""@app.route('/rings/', methods = ['POST'])
def rings():
    es.index(
        index='lord-of-the-rings',
        document={
            'character': 'Aragon',
            'quote': 'It is not this day.'
        })

    return {"status":"done"}"""