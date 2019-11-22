from datetime import *
import MySQLdb
import serial
from time import *
import socket

Lector = serial.Serial('/dev/ttyACM0',9600)

def TCP(mensaje, ip):
    server_address = (ip, 42777)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.send(mensaje.encode("utf-8"))
    sleep(0.5)
    sock.close()

mysql = MySQLdb.connect(host="localhost", passwd="2469",
                        user="root", db="Horario")
cur = mysql.cursor()
cur.execute("SELECT NFC, Inicio, Fin FROM nfc")
DataNfc = list(cur.fetchall())
cur.close()
try:
    ID = str(Lector.readline()).split("A")[1]
except:
    ID = str(Lector.readline())
Lector.reset_input_buffer()
print (ID)
for x in DataNfc:
    if ID == x[0]:
        HIni = x[1]
        HFin = x[2]
        HActual = datetime.now().strftime('%H:%M')
        HIni = datetime.strptime(HIni, '%H:%M')
        HFin = datetime.strptime(HFin, '%H:%M')
        HActual = datetime.strptime(HActual, '%H:%M')
        if HIni <= HActual and HActual <= HFin:
            print ("Acceso Concedido")
        print (HFin - HIni)
        TCP('7', '192.168.43.127')
        sleep(2)
        TCP('g', '192.168.43.127')
if ID == 'Cerrar':
    print ("Aqui prro")
