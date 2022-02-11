## this script will be run every day by server
import requests

res = requests.post('http://127.0.0.1:5001/send_all')  # sent to middleware second ms museo, data, e utente