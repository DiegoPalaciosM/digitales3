import socket, time, serial, threading, MySQLdb, datetime
global NFCAuto, ID
NFCAuto = 1
ID = 0

def TCP(mensaje, ip):
    server_address = (ip, 42777)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.send(mensaje.encode("utf-8"))
    time.sleep(0.5)
    sock.close()

def NFCAOD():
    while NFCAuto:
        Lector = serial.Serial('/dev/ttyACM0', 9600)
        mysql = MySQLdb.connect(host="localhost", passwd="2469",
                                user="root", db="Horario")
        cur = mysql.cursor()
        cur.execute("SELECT NFC FROM nfc")
        DataNfc = list(cur.fetchall())
        cur.close()
        txt = str(Lector.readline())
        print (txt)
        ID = txt.split("A")[1]
        Lector.reset_input_buffer()
        Lector.close()
        for x in DataNfc:
            if ID == x[0]:
                TCP('7', '192.168.0.6')
                time.sleep(2)
                TCP('g', '192.168.0.6')
    return ID

def AOD():
    global data
    data = []
    ip = '192.168.0.13'
    dion = {'L1-General': '1', 'L2-Industrial': '2', 'L3-Materiales': '3',
            'L4-Electromedicina': '4', 'L5-Telecomunicaciones': '5', 'L6-Software': '6'}
    dioff = {'L1-General': 'a', 'L2-Industrial': 'b', 'L3-Materiales': 'c',
             'L4-Electromedicina': 'd', 'L5-Telecomunicaciones': 'e', 'L6-Software': 'f'}

    Horas = {'1': 'Lunes, LFin', '2': 'Martes, MaFin', '3': 'Miercoles, MiFin',
             '4': 'Jueves, JuFin', '5': 'Viernes, ViFin', '6': 'Sabado, SaFin'}
    DiaW = datetime.datetime.now().strftime("%w")
    HoraA = datetime.datetime.now().strftime("%H:%M")
    HoraP = 0


    def Automatico():
        while True:
            if len(data) != 0:
                for x in data:
                    if x[1] == HoraA:
                        TCP(dion[x[0]], ip)
                    if x[2] == HoraA:
                        TCP(dioff[x[0]], ip)

    Auto = threading.Thread(target=Automatico,args=data)
    Auto.start()

    while True:
        if HoraA != HoraP:
            mysql = MySQLdb.connect(host="localhost", passwd="2469",
                                    user="root", db="Horario")
            cur = mysql.cursor()
            cur.execute(("SELECT Laboratorio, {} FROM uno").format(Horas[DiaW]))
            data = list(cur.fetchall())
            cur.close()
        HoraP = HoraA
        HoraA = datetime.datetime.now().strftime("%H:%M")

NFCAOD()
