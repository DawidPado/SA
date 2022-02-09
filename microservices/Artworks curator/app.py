from flask import Flask
from flask import jsonify
from flask import request
import sqlite3
from itsdangerous import json
import requests

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/artworks/index")
def index():
    con = sqlite3.connect('artworks.db')
    try:
        with con:
            artworks = []
            #select all artworks of one museum 
            results = con.execute("SELECT * FROM artworks").fetchall()
            for item in results:
                    artwork = {
                                "x":item[1],
                                "y":item[2],
                                "z":item[3],
                                "accessible":item[4],
                                "musueum_id":item[5],
                                "author":item[6],
                                "year":item[7],
                                "title":item[8],
                                "description":item[9],
                                "image_path":item[10]
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
    con = sqlite3.connect('artworks.db')
    try:
        with con:
            artworks = []
            #select all artworks of one museum 
            results = con.execute("SELECT * FROM artworks WHERE museum_id = ?", [museum_id]).fetchall()
            if(not results):
                for item in results:
                        artwork = {
                                    "x":item[1],
                                    "y":item[2],
                                    "z":item[3],
                                    "accessible":item[4],
                                    "museum_id":item[5],
                                    "author":item[6],
                                    "year":item[7],
                                    "title":item[8],
                                    "description":item[9],
                                    "image_path":item[10]
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
    con = sqlite3.connect('artworks.db')
    try:
        with con:
            #select all artworks of one museum 
            result = con.execute("SELECT * FROM artworks WHERE id = ?", [id]).fetchone()
            if(result!=None):
                artwork = {
                                    "x":result[1],
                                    "y":result[2],
                                    "z":result[3],
                                    "accessible":result[4],
                                    "museum_id":result[5],
                                    "author":result[6],
                                    "year":result[7],
                                    "title":result[8],
                                    "description":result[9],
                                    "image_path":result[10]
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
        con = sqlite3.connect('artworks.db')
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
        getartwork = requests.get("http://127.0.0.1:5000/artworks/show/"+str(id))
        if(getartwork.json()["success"]==True):
            con = sqlite3.connect('artworks.db')
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
        con = sqlite3.connect('artworks.db')
        with con:
            getartwork = requests.get("http://127.0.0.1:5000/artworks/show/"+str(id))
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
    pass