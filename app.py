from flask import Flask
from flask import request
import requests
import json

app = Flask(__name__)
@app.route('/serveur/', methods = ['POST'])
#le serveur écoute sur la raspi
def serveur():
    if request.method == 'POST':
        msg = request.form['reqToServer']
        print(msg)
        return ("Le serveur a bien reçu la requete depuis la raspi")
    return ("Echec de réception de la requête depuis la raspi")

@app.route('/envoi_instruction/', methods = ['POST'])
def envoi_instruction():

    msg = {'reqToArduino': "requeteToArduino"}
    # Envoyer les paquets a la raspi
    r = requests.post("http://127.0.0.1:5000/write_port_serie/", data=msg)
    print(r.text)

if __name__ == '__main__':
    app.run(debug=True)




