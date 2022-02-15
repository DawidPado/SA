import requests
import random
import string
from twisted.internet import task, reactor
import sqlite3

timeout = 5.0 # Sixty seconds
positions = []
data = {
    "id":"",
    "position":{
    "x":0,
    "y":0,
    "z":0
    }
}
def simulatePositions():
    try:
        con = sqlite3.connect('./microservices/middleware/reservations.db')
        with con:
            reservations = con.execute('SELECT * FROM reservations').fetchall()
            positions = []
            for reservation in reservations:
                position = {
                    "id":reservation[0],
                    "x": random.randint(0,10),
                    "y": random.randint(0,10),
                    "z": random.randint(0,10)
                }
                positions.append(position)
            museum = {"museum":1}
            data = [positions,museum]
            r = requests.post('http://127.0.0.1:5010/sendpositions', json=data)
            print(r.json())
    except sqlite3.Error as er:
        error="simulating positions went wrong: " + ' '.join(er.args)
        print(error)
    
l = task.LoopingCall(simulatePositions)
l.start(timeout) # call every sixty seconds

reactor.run()