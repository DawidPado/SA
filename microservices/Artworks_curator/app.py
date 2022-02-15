from math import sqrt
from flask import Flask
from flask import jsonify
from flask import request
import sqlite3
from itsdangerous import json
import requests
import json
from sys import stderr

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

def distanceCalc(user,item):
    x1 = user["x"]
    x2 = item["x"]
    y1 = user["y"]
    y2 = item["y"]
    z1 = user["z"]
    z2 = item["z"]
    distance = sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    return distance

@app.route("/")
def hello():
    return ("Ciao")

@app.route("/artworks/index")
def index():
    con = sqlite3.connect('./microservices/Artworks_curator/artworks.db')
    try:
        with con:
            artworks = []
            #select all artworks of one museum 
            results = con.execute("SELECT * FROM artworks").fetchall()
            for item in results:
                    artwork = {
                                "id":item[0],
                                "x":item[1],
                                "y":item[2],
                                "z":item[3],
                                "accessible":item[4],
                                "musueum_id":item[5],
                                "author":item[6],
                                "year":item[7],
                                "title":item[8],
                                "description":item[9],
                                "image_path":item[10],
                                "watchtime":item[11]
                                }
                    artworks.append(artwork)
            #send successful response
            resp = jsonify(artworks = artworks)
            resp.status_code = 200
    #SQL exception handler
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="/index went wrong: " + ' '.join(er.args))
        resp.status_code = 500

    con.close()
    return resp

@app.route("/artworks/index/<museum_id>")
def index_by_museum(museum_id):
    con = sqlite3.connect('./microservices/Artworks_curator/artworks.db')
    try:
        with con:
            artworks = []
            #select all artworks of one museum 
            results = con.execute("SELECT * FROM artworks WHERE museum_id = ?", [museum_id]).fetchall()
            if(results):
                for item in results:
                        artwork = {"id":item[0],
                                    "x":item[1],
                                    "y":item[2],
                                    "z":item[3],
                                    "accessible":item[4],
                                    "museum_id":item[5],
                                    "author":item[6],
                                    "year":item[7],
                                    "title":item[8],
                                    "description":item[9],
                                    "image_path":item[10],
                                    "watchtime":item[11]
                                    }
                        artworks.append(artwork)
                #send successful response
                resp = jsonify(artworks = artworks)
                resp.status_code = 200
            else:
                resp = jsonify(success=False, error="ID not found")
                resp.status_code = 404
    #SQL exception handler
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="/index/museum went wrong: " + ' '.join(er.args))
        resp.status_code = 500

    con.close()
    return resp

@app.route("/artworks/show/<id>")
def show(id):
    con = sqlite3.connect('./microservices/Artworks_curator/artworks.db')
    try:
        with con:
            #select all artworks of one museum 
            result = con.execute("SELECT * FROM artworks WHERE id = ?", [id]).fetchone()
            if(result!=None):
                artwork = {         
                                    "id":result[0],
                                    "x":result[1],
                                    "y":result[2],
                                    "z":result[3],
                                    "accessible":result[4],
                                    "museum_id":result[5],
                                    "author":result[6],
                                    "year":result[7],
                                    "title":result[8],
                                    "description":result[9],
                                    "image_path":result[10],
                                    "watchtime":result[11]
                                    }
                resp = jsonify(artwork = artwork, success=True, error="none")
                resp.status_code = 200
            else:
                resp = jsonify(success=False, error="ID not found")
                resp.status_code = 404
    #SQL exception handler
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="/show/<id> went wrong: " + ' '.join(er.args))
        resp.status_code = 500
    return resp

@app.route("/artworks/manage/create", methods = ["POST"])
def create():
    artwork = request.json["artwork"]
    x = artwork["x"]
    y = artwork["y"]
    z = artwork["z"]
    accessible = artwork["accessible"]
    museum_id = artwork["museum_id"]
    author = artwork["author"]
    year = artwork["year"]
    title = artwork["title"]
    description = artwork["description"]
    path = artwork["image_path"]
    try:
        con = sqlite3.connect('./microservices/Artworks_curator/artworks.db')
        with con:
            con.execute('''
                        INSERT INTO artworks 
                        (x_coord, 
                        y_coord, 
                        z_coord, 
                        accessible, 
                        museum_id, 
                        author, 
                        year,
                        title, 
                        description, 
                        image_path) 
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)    
                        ''', [x,y,z,accessible,museum_id,author,year,title,description,path])
            resp = jsonify(success=True, error="none")
            resp.status_code = 201
    #SQL exception handler
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="/artworks/manage/create went wrong: " + ' '.join(er.args))
        resp.status_code = 500
    return resp

@app.route("/artworks/manage/update", methods = ["POST"])
def update():
    artwork = request.json["artwork"]
    id = artwork["id"]
    x = artwork["x"]
    y = artwork["y"]
    z = artwork["z"]
    accessible = artwork["accessible"]
    museum_id = artwork["museum_id"]
    author = artwork["author"]
    year = artwork["year"]
    title = artwork["title"]
    description = artwork["description"]
    path = artwork["image_path"]
    try:
        getartwork = requests.get("http://127.0.0.1:5005/artworks/show/"+str(id))
        if(getartwork.json()["success"]==True):
            con = sqlite3.connect('./microservices/Artworks_curator/artworks.db')
            with con:
                con.execute('''
                            UPDATE artworks 
                            SET 
                            x_coord = ?, 
                            y_coord = ?, 
                            z_coord = ?, 
                            accessible = ?, 
                            museum_id = ?, 
                            author = ?, 
                            year = ?,
                            title = ?, 
                            description = ?, 
                            image_path = ?
                            WHERE id = ?    
                            ''', [x,y,z,accessible,museum_id,author,year,title,description,path,id])
                resp = jsonify(success=True, error="none")
                resp.status_code = 200
        else:
            resp = jsonify(success=False, error="ID not found")
            resp.status_code = 404
    #SQL exception handler
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="/artworks/manage/update went wrong: " + ' '.join(er.args))
        resp.status_code = 500
    return resp

@app.route("/artworks/manage/delete/<id>", methods = ["POST"])
def delete(id):
    try:
        con = sqlite3.connect('./microservices/Artworks_curator/artworks.db')
        with con:
            getartwork = requests.get("http://127.0.0.1:5005/artworks/show/"+str(id))
            if(getartwork.json()["success"]==True):
                con.execute("DELETE FROM artworks WHERE id = ?",[id])
                resp = jsonify(success=True, error="none")
                resp.status_code = 200
            else:
                resp = jsonify(success=False, error="ID not found")
                resp.status_code = 404
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="/artworks/manage/delete went wrong: " + ' '.join(er.args))
        resp.status_code = 500
    return resp       
    
@app.route("/artworks/near/<user_id>")
def getnear(user_id):
    try:
        con = sqlite3.connect("./microservices/Artworks_curator/artworks.db")
        with con:
            artworks_ids = con.execute("SELECT * FROM near_artworks WHERE user_id = ?", [user_id]).fetchall()
            if(artworks_ids):
                nearartworks = []
                for artwork_id in artworks_ids:
                    artwork = requests.get("http://127.0.0.1:5005/artworks/show/" + str(artwork_id[1]))
                    artwork = artwork.json()["artwork"]
                    nearartworks.append(artwork)
                resp = jsonify(artworks = nearartworks)
                resp.status_code = 200
            else:
                resp = jsonify(success = False, error = "No nearby artworks")
                resp.status_code = 404    
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="Get nearby artworks went wrong: " + ' '.join(er.args))
        resp.status_code = 500
    return resp

#endpoint which the localizator microservice uses to send the positions of all the users inside all the museums
@app.route("/positions", methods =["POST"])
def positions():
    #Gather all the positions from the localizator
    positions = request.json

    #set distance threshold
    THRESHOLD = 2.0
    try:
        con = sqlite3.connect('./microservices/Artworks_curator/artworks.db')
        with con:
            #print("entered with", file=stderr)
            #everytime the nearby artworks change, so reset the near_artworks table
            con.execute("DELETE FROM near_artworks")
            i = 1
            #print("executed delete all", file=stderr)
            #for each museum (1,2,3) get its artworks...
            while i <= 3:
                get_museum_artworks = requests.get("http://127.0.0.1:5005/artworks/index/"+str(i)).json()["artworks"]
                #print("got artworks of museum", file=stderr)
                #print("artworks are non empty: " + str(len(get_museum_artworks)), file=stderr)
                #... and for each user... 
                for item in positions:
                    user = item
                    #print("entered for item in positions", file=stderr)
                    #... if the user is inside that museum and if that museum has any artworks...
                    #print("user location: " + str(user["museum_id"]) + " i: " + str(i), file=stderr)
                    #print(type(user["museum_id"]), file=stderr)
                    #print(type(i), file=stderr)
                    if(int(user["museum_id"])==i):
                        #print(user["museum_id"]==i, file=stderr)
                        #... for each artwork... 
                        for artwork in get_museum_artworks:
                            distance = distanceCalc(user,artwork)
                            print("calculated distance: " + str(distance), file=stderr)
                            #... if the user is nearby...
                            if(distance<=THRESHOLD):
                                print("distance smaller than threshold", file=stderr)
                                #insert a new row in the near_artworks table
                                con.execute("INSERT INTO near_artworks (user_id, artwork_id) VALUES (?,?)", [user["id"],artwork["id"]])
                                #increment the watchtime for that artwork in the artworks table
                                con.execute('''UPDATE "artworks"
                                                    SET "watchtime" = "watchtime" + 1
                                                    WHERE id = ?;''', [artwork["id"]])   
                        
                i+=1
            resp = jsonify(success=True, error="none")
            resp.status_code = 200
    except sqlite3.Error as er:
        resp = jsonify(success=False, error="Insert into near_artworks went wrong: " + ' '.join(er.args))
        resp.status_code = 500

    return resp

if __name__ == "__main__":
    app.run(debug=True, port=5005)