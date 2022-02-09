import requests
import random
from flask import jsonify
import json

i = 1
positions = []
while i<=1500:
    position = {
        "id":i,
        "museum_id":random.randint(1,3),
        "x":random.randint(0,10),
        "y":random.randint(0,10),
    }
    positions.append(position)
    i+=1
requests.post("http://127.0.0.1:5000/positions", json=positions)