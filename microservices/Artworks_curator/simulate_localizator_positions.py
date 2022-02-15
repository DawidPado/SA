import requests
import random
from flask import jsonify
import json
from twisted.internet import task, reactor

timeout = 2.0 # Two seconds
def sendPositions():
    i = 1
    counter = 1
    positions = []
    while i<=3:
        j=1
        while j<=500:
            position = {
                "id":counter,
                "museum_id":i,
                "x":random.randint(0,10),
                "y":random.randint(0,10),
                "z":random.randint(0,10)
            }
            positions.append(position)
            j+=1
            counter += 1
        i+=1

    requests.post("http://127.0.0.1:5005/positions", json=positions)

l = task.LoopingCall(sendPositions)
l.start(timeout) # call every two seconds

reactor.run()