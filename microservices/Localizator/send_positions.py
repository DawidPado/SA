import requests
import random
from flask import jsonify
import json
from twisted.internet import task, reactor
import sqlite3

timeout = 5.0 # Two seconds
def sendPositions():
    try:
        con = sqlite3.connect("./microservices/Localizator/database.db")
        with con:
            results = con.execute("SELECT * FROM positions").fetchall()
            if(results):
                positions = []
                for result in results:
                    position = {
                        "museum_id": result[1],
                        "x": result[2],
                        "y": result[3],
                        "z": result[4],
                        "id": result[5]
                    }
                    positions.append(position)
                r = requests.post("http://127.0.0.1:5005/positions", json=positions)
                print(r.json())
    except sqlite3.Error as er:
        error="send positions from localizator went wrong: " + ' '.join(er.args)
        print(error)     
    

l = task.LoopingCall(sendPositions)
l.start(timeout) # call every two seconds

reactor.run()