import sqlite3
import sys
import traceback
import random
import names
import string
from random_word import RandomWords
from lorem_text import lorem

r = RandomWords()

con = sqlite3.connect('artworks.db')

try:
    with con:
        con.execute('''
                    CREATE TABLE IF NOT EXISTS artworks 
                    (id integer primary key, 
                    x_coord integer, 
                    y_coord integer, 
                    z_coord integer, 
                    accessible integer, 
                    museum_id integer, 
                    author text, 
                    year text,
                    title text, 
                    description text, 
                    image_path text)''')
        
        i = 0
        while i<50:
            x = random.randint(0,10)
            y = random.randint(0,10)
            z = random.randint(0,10)
            museum_id = random.randint(1,3)
            author = names.get_last_name()
            year = random.randint(1900,2000)
            title = lorem.words(1)
            description = lorem.paragraph()
            path = "/paintings/" + author + "/" + title
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
                        (?, ?, ?, 1, ?, ?, ?, ?, ?, ?)    
                        ''', [x,y,z,museum_id,author,year,title,description,path])
            print(str(i) + ") Done")
            i += 1
except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

con.close()