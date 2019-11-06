def AOD():
    import threading
    import serial
    import time
    import MySQLdb
    import datetime
    import Acciones
    import time

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
                        Acciones.TCP(dion[x[0]], ip)
                    if x[2] == HoraA:
                        Acciones.TCP(dioff[x[0]], ip)

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
            print (data)
        HoraP = HoraA
        HoraA = datetime.datetime.now().strftime("%H:%M")
