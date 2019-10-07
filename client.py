import socket
import threading
from tkinter import  *
from tkinter.filedialog import askopenfilename
from time import sleep
class connessione:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8988

        ip = "192.168.1.10"
        """ Questo è l'ip del mio pc """
        self.s.connect((ip, port))

    def riproduciMusica(self):
        self.s.send("avvia playlist dormire".encode("ascii"))

    def cmd(self,finestra):
        button1.destroy()
        button2.destroy()
        button3.destroy()
        button4.destroy()
        self.s.send("cmd".encode("ascii"))
        output1 =Label(finestra, text="output:")
        output2 = Label(finestra,text= "output")
        input = Entry(finestra)
        bottone = Button(finestra, text="esegui comando", command=lambda: eseguiComando(input.get(), output2))

        output1.grid(row=0,column=0)
        output2.grid(row=0, column=1)
        bottone.grid(row=1, column=0)
        input.grid(row=1, column=1)
        def eseguiComando(input,output2):
            self.s.send(input.encode('ascii'))
            sleep(1)
            text = self.s.recv(1024).decode('ascii')
            output2.destroy()
            output2 = Label(finestra,text= text)
            output2.grid(row=0, column=1)


    def ricevimsg(self):
        clientAttivo = True
        serverAttivo = False
        while clientAttivo and (not serverAttivo):
            try:
                msg = self.s.recv(1024).decode('ascii')
                print(msg)
            except:
                print('Server offline,premi invio per disconnetterti')
                serverAttivo = True

    def mandaFile(self):
        self.s.send("manda".encode())
        nomeFile = askopenfilename()
        f = open(nomeFile, 'rb')
        l = f.read(1024)
        while (l):
            self.s.send(l)
            print(repr(l))
            l = f.read(1024)
        f.close()

    def turn_off(self):
        self.s.send("Spegni".encode('ascii'))

    def main(self):

        clientAttivo = True
        conn = connessione()
        threading.Thread(target=conn.ricevimsg, args=()).start()
        while clientAttivo:

            msg = input('>>')
            if msg.__contains__("manda"):
                self.s.send(msg.encode('ascii'))
                connessione.mandaFile(self.s)
            else:
                self.s.send(msg.encode('ascii'))
            """da qui faccio i comandi che voglio,ma li faccio elaborare al pc,essendo più veloce"""

def bottone(finestra,color,numero):
    pass

def creaFinestra(main):
    #dichiarazione variabili normali
    color = "#ffffff"
    width = 960
    height = 539
    widthFinestra = 700
    heightFinestra = 400
    c = "ciao"
    # fine dichiarazione variabili normali

    #inizio dichiarazione finestra
    global finestra
    finestra = Tk()
    finestra.title("H.A.V.A")
    finestra.resizable(True, True)
    finestra.geometry("1920x1080")
    finestra.configure(background=color)
    #fine dichiarazione finestra

    #dichiarazione immagini
    immagine_canzone = PhotoImage(file="Song.png")
    immagine_trasferimento_dati = PhotoImage(file="data-transfer-pc-pc.png")
    immagine_turn_off = PhotoImage(file="power-off1.png")
    immagine_putty = PhotoImage(file="putty.png")
    #fine dichiarazione immagini

    #dichiarazione bottoni
    global button1
    button1 = Button(finestra,image = immagine_canzone, bd=0, background=color, relief="flat", command=lambda: main.riproduciMusica(),
                     fg="black", width=960, height=539, textvariable=c)
    global button2
    button2 = Button(finestra,image = immagine_trasferimento_dati, bd=0, background=color, relief="flat", command=lambda: main.mandaFile(),
                     fg="black", width=width, height=height, textvariable=c)
    global button3
    button3 = Button(finestra,image = immagine_turn_off, bd=0, background=color, relief="flat", command=lambda: main.turn_off(),
                     fg="black", width=width, height=height, textvariable=c)
    global button4
    button4 = Button(finestra,image = immagine_putty, bd=0, background=color, relief="flat", command=lambda: main.cmd(finestra),
                     fg="black", width=width, height=height, textvariable=c)
    #fine dichiarazione bottoni

    button1.grid(row=0, column=0)
    button2.grid(row=0, column=1)
    button3.grid(row=1, column=0)
    button4.grid(row=1, column=1)




    #fine finestra
    finestra.mainloop()







if __name__ == "__main__":
    main = connessione()
    creaFinestra(main)
    main.main()


