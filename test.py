import sqlite3
import requests
import datetime

totaltime = 0
counter = 0
ids = []
try:
    con = sqlite3.connect("./microservices/middleware/reservations.db")
    with con:
        con.execute("UPDATE reservations SET checkin = 0")
        results = con.execute("SELECT * FROM reservations WHERE checkin = 0")
        for result in results:
            ids.append(result[0])

    i = 0
    while i<40:
        for id in ids:
            start_time = datetime.datetime.now()
            r = requests.post("http://127.0.0.1:5010/reservations/checkin", json = {"id": id})
            end_time = datetime.datetime.now()
            print(r.json())
            time_diff = (end_time - start_time)
            execution_time = time_diff.total_seconds() * 1000
            print(execution_time)
            totaltime += execution_time
            counter += 1
        i += 1        
    print("Total execution time for " + str(counter) + " executions: " + str(totaltime) + " milliseconds")
    print("Average checkin time for " + str(counter) + " executions: " + str(totaltime/counter) + " milliseconds")
except sqlite3.Error as er:
        pass

