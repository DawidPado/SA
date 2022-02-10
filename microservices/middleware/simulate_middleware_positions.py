import requests
import random
import string
from twisted.internet import task, reactor

timeout = 5.0 # Sixty seconds
data = {
    "id":"",
    "position":{
    "x":0,
    "y":0,
    "z":0
    }
}
def simulatePositions():
    data["id"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    data["position"]["x"] = random.randint(0, 100)
    data["position"]["y"] = random.randint(0, 100)
    data["position"]["z"] = random.randint(0, 100)
    r = requests.post('http://127.0.0.1:5000/sendposition', json=data)
    print(r.json())
    pass

l = task.LoopingCall(simulatePositions)
l.start(timeout) # call every sixty seconds

reactor.run()