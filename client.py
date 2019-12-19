import sys
import json
import requests
from serial import *
# import serial
import time
from flask import Flask
from flask import request

TIME_OUT_READ = 1
TIME_OUT_WRITE = 1

app = Flask(__name__)
# fonction écoute sur l'arduino
def read_port_serie(ser):
    time.sleep(0.1)
    chaine=ser.readline()
    msg = {'reqToServer': ser.readline()}
    #Envoyer les paquets au serveur
    r = requests.post("http://192.168.43.224:9236/", data=msg)
    print(r.text)


# fonction pour l'envoi de données
@app.route('/write_port_serie/', methods = ['POST'])
def write_port_serie(ser):
    # si la raspi reçoit des instruction depuis le serveurs
    if request.method == 'POST': #changer cette condition
        chaine = request.form['reqToArduino']
        ser.write(chaine.encode('ascii'))
        time.sleep(0.1)
        return ("Raspi a bien recu l instruction depuis de seveur")
    return ("Echec de reception depuis le serveur")



with Serial(port="/dev/ttyACM0", baudrate=9600, timeout=TIME_OUT_READ, writeTimeout=TIME_OUT_WRITE) as port_serie:
    if port_serie.isOpen():
        # write_port_serie(port_serie,"HELLO")
        # read_port_serie(port_serie)
        print("port serie ouvert")
        while True:
                write_port_serie(port_serie)
                #print(read_port_serie(port_serie))

                #lecture du port serie et envoie de requete au serveur
                read_port_serie(port_serie)
        else:
            print("port serie non ouvert")

