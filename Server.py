import socket
import webbrowser
import subprocess
import os
from zlib import decompress


def riceviFile(user):
    with open('received_file.png', 'wb') as f:
        while True:
            data = user.recv(1024)
            print(data)
            if not data:
                break
            f.write(data)
        f.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAttivo = True
ip = "192.168.1.10"
port = 8988
c = 0
s.bind((ip, port))
s.listen()
print('Server Online...')
print('Indirizzo ip del server::%s'%ip)

user, indirizzo = s.accept()
user.send('Connessione avvenuta'.encode('ascii'))
while serverAttivo:
    comando = user.recv(1024).decode('ascii')
    if comando.__contains__("avvia"):
        comando = comando.replace("avvia ","")

        if comando.__contains__("playlist"):
            comando = comando.replace("playlist ", "")

            if comando.__contains__("dormire"):
                webbrowser.open("https://www.youtube.com/watch?v=OSap4nsa_rY&")
    elif comando.__contains__("Spegni"):
        os.system("shutdown /r /t 1")
    elif comando.__contains__("manda"):
        riceviFile(user)
    elif comando.__contains__("cmd"):
        cmd = True
        while cmd:
            cmd = user.recv(1024).decode("ascii")
            risposta = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr = subprocess.PIPE)
            data = risposta.stdout + risposta.stderr
            print(data.decode())
            user.send(data)










