import requests
import random
import string
from twisted.internet import task, reactor

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
    positions = []
    i = 0
    while i<500:
        position = {
            "id":''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            "x": random.randint(0,10),
            "y": random.randint(0,10),
            "z": random.randint(0,10)
        }
        positions.append(position)
    r = requests.post('http://127.0.0.1:5000/sendposition', json=positions)
    print(r.json())
    

l = task.LoopingCall(simulatePositions)
l.start(timeout) # call every sixty seconds

reactor.run()