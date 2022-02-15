import datetime
import sqlite3

from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, session
from flask_cors import CORS
from flask_restful import Api, reqparse
import requests
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'
api = Api(app)
parser = reqparse.RequestParser()
CORS(app)
es = Elasticsearch()




@app.route('/ciao', methods=['POST'])
def ciao():  # put application's code here
    print("ciao")
    return{'email':session['email']}

@app.route('/positions/update',methods = ["POST"])
def localizator():  # put application's code here
    positions = request.json[0]
    museum_id = request.json[1]["museum"]
    try:
        statement = "INSERT INTO positions (museum, x, y, z, booking_id) VALUES (?,?,?,?,?)"
        con = sqlite3.connect('./microservices/Localizator/database.db')
        with con:
            con.execute("DELETE FROM positions WHERE museum = ?",[museum_id])
            for position in positions:
                values = [museum_id,position["x"],position["y"],position["z"],position["id"]]
                con.execute(statement,values)
            resp = jsonify(success = True, error="none")
            resp.status_code = 200
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="/positions/update went wrong: " + ' '.join(er.args))
        resp.status_code = 500
    return resp

if __name__ == '__main__':
    app.run(host="localhost", port=5003, debug=True)