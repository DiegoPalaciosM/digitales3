import socket, time
class EstadoLaboratorio:
    def __init__(self, Laboratorio, Estado, Hora):
        self.Laboratorio = Laboratorio
        self.Estado = Estado
        self.Hora = Hora

    def ActualizarEstado(Estado, Hora):
        self.Estado = Estado
        self.Hora = Hora


L1 = EstadoLaboratorio('L1-General', 'Cerrado', '12:00')
L2 = EstadoLaboratorio('L2-Industrial', 'Cerrado', '12:00')
L3 = EstadoLaboratorio('L3-Materiales', 'Cerrado', '12:00')
L4 = EstadoLaboratorio('L4-Electomedicina', 'Cerrado', '12:00')
L5 = EstadoLaboratorio('L5-Telecomunicaciones', 'Cerrado', '12:00')
L6 = EstadoLaboratorio('L6-Software', 'Cerrado', '12:00')
Automatizacion = EstadoLaboratorio('Automatizacion', 'Cerrado', '12:00')


def TCP(mensaje, ip):
    server_address = (ip, 42777)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.sendall(mensaje.encode("utf-8"))
    for x in dion:
        if mensaje == dion[x]:
            print ("Abrir")
        elif mensaje == dioff[x]:
            print ("Cerrar")
    time.sleep(0.5)
    sock.close()

dion = {'L1-General': '1', 'L2-Industrial': '2', 'L3-Materiales': '3',
        'L4-Electromedicina': '4', 'L5-Telecomunicaciones': '5', 'L6-Software': '6','Automatizacion': '7'}
dioff = {'L1-General': 'a', 'L2-Industrial': 'b', 'L3-Materiales': 'c',
         'L4-Electromedicina': 'd', 'L5-Telecomunicaciones': 'e', 'L6-Software': 'f','Automatizacion': 'g'}

TCP('g','192.168.0.13')

print (dion)
