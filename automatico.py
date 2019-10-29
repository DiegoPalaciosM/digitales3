import threading, serial, time, MySQLdb, datetime, time

global laboratorio, laboratorio1, hora, hora1, data
laboratorio = []
laboratorio1 = hora1 = data = ''
hora = datetime.datetime.now().strftime('%H:%M')
dias = {0:2,1:3,2:4,3:5,4:6,5:7}
ard = {'L1-General':'1','L2-Industrial':'2','L3-Materiales':'3'}

def paralelo():
    while True:
        if len(laboratorio) != 0:
            for x in laboratorio:
                puerta = serial.Serial('/dev/ttyACM0',9600)
                puerta.write(ard[x].encode())
                puerta.close()
                time.sleep(1)
                laboratorio.remove(x)

a = threading.Thread(target=paralelo)
a.start()

while True:
    dia = dias[time.localtime()[6]]
    if hora != hora1:
        mysql = MySQLdb.connect('localhost','root','2469','Horario')
        cur = mysql.cursor()
        cur.execute("SELECT * FROM uno")
        data = cur.fetchall()
        cur.close()
        for x in data:
            if (x[dia]) == hora:
                laboratorio.append(x[8])
                print(laboratorio)
                print(len(laboratorio))
    hora1 = hora
    hora = datetime.datetime.now().strftime('%H:%M')
