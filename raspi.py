from threading import Thread
import time
from serial import *
from datetime import datetime
import requests
from flask import Flask
import calendar
import time



app = Flask("RT")


#Fonction qui retourne le timestamp
def time_stamp():
    timestamp = str(calendar.timegm(time.gmtime()))
    return timestamp

#Fonction qui retourne la date
def date_function():
    date = datetime.now()
    date = str(date.day) + "/" + str(date.month) + "/" + str(date.hour) + " -- " + str(date.time().hour) + ":" + str(date.time().minute) + ":" + str(date.time().second)
    return date


#Fonction quii perlet de logger
def log_function(msg):
    date = date_function()
    log= date + '--'+ msg

    #Ecrire dans un fichier log
    fichier = open("data.txt", "r")
    fichier.write(log)
    fichier.close()


# fonction pour la recepetion de message
def read_port_serie(p):
    #time.sleep(0.2)
    chaine = p.readline()
    return str(chaine)[2:len(chaine)]


# fonction pour l'envoye de donne
def write_port_serie(p, chaine):
    # si la raspi reçoit des instruction depuis le serveurs
    p.write(chaine.encode('ascii'))
    # if request.method == 'POST':  # changer cette condition
    #     chaine = request.form['reqToArduino']
    #time.sleep(0.2)
    #     return ("Raspi a bien recu l instruction depuis de seveur")
    # return ("Echec de reception depuis le serveur")


class Arduino(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        self.port=port
        self.send_message = False
        self.message = None

    def do_send_message(self, msg):
        self.send_message = True
        self.message = msg

    def run(self):
        while True:
            if self.send_message:
                #write_port_serie(self.port, self.message)
                self.send_message = False
                self.message = None
            chaine = read_port_serie(self.port)
            if chaine is not None and 'ALERT' in chaine and chaine is not '':

                # informer l'arduino que la raspi a bien recu l'alerte
                print(chaine)
                write_port_serie(self.port, "ACK")

                #envoyer au serveur
                timeS = time_stamp()
                val= chaine + ',' + timeS+ ',A1'
                msg = {'reqToServer': val}

                r = None
                url ="http://192.168.43.224:9236/server"
                try:

                    r = requests.post(url, data=msg)
                    print(url)
                except Exception as e:
                    print(e)
                if r is not None and r.status_code is 200:
                   # return r.content
                    print(r.text)
                else:
                    ## TODO PING REGULARLY
                    log_function(chaine)
                    #return '{"status":"error"}'




TIME_OUT_READ = 1
TIME_OUT_WRITE = 1
port = Serial(port="/dev/ttyACM0", baudrate=9600, timeout=TIME_OUT_READ, writeTimeout=TIME_OUT_WRITE)

a = Arduino(port)
print(type(a).__name__)
a.start()
print("le main")


@app.route('/')
def index():
    return "hello"


@app.route('/test')
def test():
    return "test"


@app.route('/msg/<content>')
def message(content):
    #a.do_send_message(content)
    write_port_serie(port, content)
    return "sent"

app.run(host='0.0.0.0')
