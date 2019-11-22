from flask import *
from flask_mysqldb import *
import socket
from time import *
import serial
from threading import *
import MySQLdb
from datetime import *
import sys
import netifaces as ni


class EstadoLaboratorio:
    def __init__(self, Laboratorio, Estado, Hora, Tipo, Clase):
        self.Laboratorio = Laboratorio
        self.Estado = Estado
        self.Hora = Hora
        self.Tipo = Tipo
        self.Clase = Clase

    def ActualizarEstado(self, Estado, Hora, Tipo, Clase):
        self.Estado = Estado
        self.Hora = Hora
        self.Tipo = Tipo
        self.Clase = Clase

L1 = EstadoLaboratorio('L1-General', 'Cerrado', '12:00', "Horario", "Libre")
L2 = EstadoLaboratorio('L2-Industrial', 'Cerrado', '12:00', "Horario", "Libre")
L3 = EstadoLaboratorio('L3-Materiales', 'Cerrado', '12:00', "Horario", "Libre")
L4 = EstadoLaboratorio('L4-Electomedicina', 'Cerrado', '12:00', "Horario", "Libre")
L5 = EstadoLaboratorio('L5-Telecomunicaciones', 'Cerrado', '12:00', "Horario", "Libre")
L6 = EstadoLaboratorio('L6-Software', 'Cerrado', '12:00', "Horario", "Libre")
Automatizacion = EstadoLaboratorio('Automatizacion', 'Cerrado', '12:00', "Horario", "Libre")

class Automatico(Thread):
    def __init__(self, Nombre, funcion, Delay):
        super(Automatico, self).__init__()
        self.estado = True
        self.funcion = funcion
        self.nombre = Nombre
        self.delay = Delay

    def stop(self):
        self.estado = False
        print ("Stop")

    def restart(self):
        self.estado = True

    def run(self):
        print (self.nombre+"Iniciado")
        while True:
            while self.estado:
                self.funcion()
                sleep(self.delay)

# Configuracion inical

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'Direccion MySQL'
app.config['MYSQL_USER'] = 'User'
app.config['MYSQL_PASSWORD'] = 'Pass'
app.config['MYSQL_DB'] = 'DB'
app.secret_key = 'Key'
mysql = MySQL(app)
ip = sys.argv[1]
print (ip)

# Direcctorio laboratorio
dion = {'L1-General': '1', 'L2-Industrial': '2', 'L3-Materiales': '3',
        'L4-Electromedicina': '4', 'L5-Telecomunicaciones': '5', 'L6-Software': '6', 'Automatizacion': '7'}
dioff = {'L1-General': 'a', 'L2-Industrial': 'b', 'L3-Materiales': 'c',
         'L4-Electromedicina': 'd', 'L5-Telecomunicaciones': 'e', 'L6-Software': 'f', 'Automatizacion': 'g'}

global Labos
Labos = {'L1-General': L1, 'L2-Industrial': L2, 'L3-Materiales': L3,
         'L4-Electromedicina': L4, 'L5-Telecomunicaciones': L5, 'L6-Software': L6, 'Automatizacion': Automatizacion}


# Pagina
@app.route('/')
def main():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM uno')
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM nfc')
    data1 = cur.fetchall()
    cur.close()
    if 'account' in session:
        acc = session['account'].title()
    else:
        acc = ''
    if 'Logged' in session:
        return render_template('abrir.html', user=acc, horarios=data, l1 = L1, l2 = L2, l3 = L3, l4 = L4, l5 = L5, l6 = L6)
    elif 'Edit' in session:
        return render_template('editar.html', user=acc, horarios=data, l1 = L1, l2 = L2, l3 = L3, l4 = L4, l5 = L5, l6 = L6)
    elif 'NFC' in session:
        return render_template('NFC.html', user=acc, horarios=data, nfcs=data1, l1 = L1, l2 = L2, l3 = L3, l4 = L4, l5 = L5, l6 = L6)
    elif 'TodoPoderoso' in session:
        return render_template('TodoPoderoso.html', user=acc, horarios=data, nfcs=data1, l1 = L1, l2 = L2, l3 = L3, l4 = L4, l5 = L5, l6 = L6)
    else:
        return render_template('nologin.html', horarios=data, l1 = L1, l2 = L2, l3 = L3, l4 = L4, l5 = L5, l6 = L6)

# Relacionado con la sesion
@app.route('/auth', methods=['POST'])
def Auth():
    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM users WHERE user = %s AND pass = %s', (user, passw))
        data = cur.fetchone()
        mysql.connection.commit()
        if data:
            if data[5] == 'Si':
                session['Edit'] = True
                session['account'] = data[3]
                return redirect(url_for('main'))
            elif data[6] == 'Si':
                session['NFC'] = True
                session['account'] = data[3]
                return redirect(url_for('main'))
            elif data[7] == 'Si':
                session['TodoPoderoso'] = True
                session['account'] = data[3]
                return redirect(url_for('main'))
            else:
                session['Logged'] = True
                session['account'] = data[3]
                return redirect(url_for('main'))
        else:
            flash('Usuario o contraseña erroneos')
            return redirect(url_for('main'))
    return redirect(url_for('main'))


@app.route('/registro', methods=['POST'])
def Registro():
    existe = 0
    if request.method == 'POST':
        user = str(request.form['user'])
        passw = str(request.form['pass'])
        cfpassw = str(request.form['cfpass'])
        nombre = str(request.form['nombre'])
        apellido = str(request.form['apellido'])
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        mysql.connection.commit()
        for x in data:
            if x[1] == user:
                existe = 1
                print ("aqui" + str(x))
                break
            else:
                existe = 0
        if existe:
            flash('Usuario ya existente')
            return redirect(url_for('main'))
        else:
            if cfpassw == passw and user != "" and nombre != "" and apellido != "":
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (user, pass, nombre, apellido) VALUES ('%s', '%s', '%s', '%s');" % (
                    user, passw, nombre, apellido))
                mysql.connection.commit()
                flash('Usuario registrado')
                return redirect(url_for('main'))
    flash('Error en el formulario de registro')
    return redirect(url_for('main'))


@app.route('/logout')
def Logout():
    session.pop('Logged', None)
    session.pop('Edit', None)
    session.pop('NFC', None)
    session.pop('TodoPoderoso', None)
    session.pop('account', None)
    return redirect(url_for('main'))

# Editar Horario
@app.route('/modificar', methods=['POST'])
def Modificar():
    if request.method == 'POST':
        if request.form['laboratorio']:
            lab = request.form['laboratorio']
            if lab != 'Seleccionar Laboratorio':
                lab = request.form['laboratorio']
            else:
                flash('Laboratorio no valido')
                return (redirect(url_for('main')))
        if request.form['lunes'] != "":
            lunes = request.form['lunes']
            lfin = request.form['lfin']
        else:
            lunes = "No"
            lfin = "No"
        if request.form['martes'] != "":
            martes = request.form['martes']
            mafin = request.form['mafin']
        else:
            martes = "No"
            mafin = "No"
        if request.form['miercoles'] != "":
            miercoles = request.form['miercoles']
            mifin = request.form['mifin']
        else:
            miercoles = "No"
            mifin = "No"
        if request.form['jueves'] != "":
            jueves = request.form['jueves']
            jufin = request.form['jufin']
        else:
            jueves = "No"
            jufin = "No"
        if request.form['viernes'] != "":
            viernes = request.form['viernes']
            vifin = request.form['vifin']
        else:
            viernes = "No"
            vifin = "No"
        if request.form['sabado'] != "":
            sabado = request.form['sabado']
            safin = request.form['safin']
        else:
            sabado = "No"
            safin = "No"
        if request.form['clase']:
            clase = request.form['clase']
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO uno (Clase, Lunes, LFin, Martes, MaFin, Miercoles, MiFin, Jueves, JuFin, Viernes, ViFin, Sabado, SaFin, Laboratorio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                        (clase, lunes, lfin, martes, mafin, miercoles, mifin, jueves, jufin, viernes, vifin, sabado, safin, lab))
            mysql.connection.commit()
            flash('Horario Actualizado')
            return (redirect(url_for('main')))
        else:
            flash('Clase no puede estar vacio')
            return (redirect(url_for('main')))


@app.route('/eliminar/<id>')
def Eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM uno WHERE id = {};'.format(id))
    mysql.connection.commit()
    flash('Entrada Eliminada')
    return redirect(url_for('main'))

# Acciones Puertas
@app.route('/abrir', methods=['POST'])
def Abrir():
    if request.method == 'POST':
        lab = request.form['laboratorio']
        if lab == 'Seleccionar Laboratorio':
            flash('Laboratorio no valido')
            return (redirect(url_for('main')))
        mensaje = dion[lab]
        TCP(mensaje, ip)
        HoraA = datetime.now().strftime("%H:%M")
        Labos[lab].ActualizarEstado("Abierto",HoraA,"Monitor", "Libre")
        flash('Seguro de %s abierto' % (lab))
    return redirect(url_for('main'))


@app.route('/cerrar', methods=['POST'])
def Cerrar():
    if request.method == 'POST':
        lab = request.form['laboratorio']
        if lab == 'Seleccionar Laboratorio':
            flash('Laboratorio no valido')
            return (redirect(url_for('main')))
        mensaje = dioff[lab]
        TCP(mensaje, ip)
        HoraA = datetime.now().strftime("%H:%M")
        Labos[lab].ActualizarEstado("Cerrado",HoraA,"Monitor", "Libre")
        flash('Seguro de %s cerrado' % (lab))
    return redirect(url_for('main'))


@app.route('/abrirauto', methods=['POST'])
def AbrirAuto():
    if request.method == 'POST':
        TCP('7', ip)
        flash('Seguro abierto')
    return redirect(url_for('main'))


@app.route('/cerrarauto', methods=['POST'])
def CerrarAuto():
    if request.method == 'POST':
        TCP('g', ip)
        flash('Seguro cerrado')
    return redirect(url_for('main'))

# NFC
@app.route('/registroNFC', methods=['POST'])
def RegistroNFC():
    try:
        if request.method == 'POST':
            name = str(request.form['nombre'])
            lastname = str(request.form['apellido'])
            code = str(request.form['code'])
            hora1 = str(request.form['ini'])
            hora2 = str(request.form['fin'])
            AutoNFC.stop()
            Lector.write(1)
            sleep(1)
            Lector.reset_input_buffer()
            Data = str(Lector.readline())
            Lector.reset_input_buffer()
            AutoNFC.restart()
            ID = Data.split("A")[1]
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM nfc")
            data = cur.fetchall()
            mysql.connection.commit()
            existe = 0
            print (data)
            for x in data:
                if int(x[4]) == int(ID) or int(x[3]) == int(code):
                    existe = 1
                    break
                else:
                    existe = 0
            if existe:
                flash('Codigo o NFC se encuentra en uso')
                return redirect(url_for('main'))
            else:
                if name != "" and lastname != "":
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO nfc (Nombre, Apellido, Codigo, NFC, Inicio, Fin) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
                        name, lastname, code, ID, hora1, hora2))
                    mysql.connection.commit()
                    flash('Usuario registrado')
                    return redirect(url_for('main'))
    except:
        flash('Error en el formulario de registro')
        return redirect(url_for('main'))

@app.route('/eliminarnfc/<id>')
def EliminarNFC(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM nfc WHERE id = {};'.format(id))
    mysql.connection.commit()
    flash('Etiqueta Eliminada')
    return redirect(url_for('main'))


# Acciones

def TCP(mensaje, ip):
    server_address = (ip, 42777)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.send(mensaje.encode("utf-8"))
    sleep(0.5)
    sock.close()


def AOD():
    Horas = {'1': 'Lunes, LFin', '2': 'Martes, MaFin', '3': 'Miercoles, MiFin',
             '4': 'Jueves, JuFin', '5': 'Viernes, ViFin', '6': 'Sabado, SaFin'}
    DiaW = datetime.now().strftime("%w")
    HoraA = datetime.now().strftime("%H:%M")
    HoraP = 0
    #Labos = {'L1-General': L1, 'L2-Industrial': L2, 'L3-Materiales': L3, 'L4-Electromedicina': L4, 'L5-Telecomunicaciones': L5, 'L6-Software': L6, 'Automatizacion': Automatizacion}
    if HoraA != HoraP:
        mysql = MySQLdb.connect(host="localhost", passwd="ldpp",
                                user="root", db="Horario")
        cur = mysql.cursor()
        cur.execute(
            ("SELECT Laboratorio, Clase, {} FROM uno").format(Horas[DiaW]))
        DataAuto = list(cur.fetchall())
        cur.close()
    HoraP = HoraA
    HoraA = datetime.now().strftime("%H:%M")
    if len(DataAuto) != 0:
        for x in DataAuto:
            if x[2] == HoraA:
                TCP(dion[x[0]], ip)
                HoraA = datetime.now().strftime("%H:%M")
                Labos[x[0]].ActualizarEstado("Abierto",HoraA,"Horario",x[1])
            if x[3] == HoraA:
                TCP(dioff[x[0]], ip)
                HoraA = datetime.now().strftime("%H:%M")
                Labos[x[0]].ActualizarEstado("Cerrado",HoraA,"Horario",x[1])

def NFC():
        mysql = MySQLdb.connect(host="localhost", passwd="ldpp",
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
                if HIni <= HActual and HActual < HFin:
                    print ("Acceso Concedido")
                    TCP('7', ip)
                    sleep(2)
                    TCP('g', ip)
        if ID == 'Cerrar':
            print ("Aqui prro")

# Test
@app.route('/test')
def TEST():
    AutoNFC.stop()
    Lector.write(1)
    sleep(2)
    text = str(Lector.readline())
    AutoNFC.restart()
    ID = text.split("A")[1]
    return ID
# Iniciar pagina
if __name__ == '__main__':
    ip_page = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
    Lector = serial.Serial('/dev/ttyACM0', 9600)
    Lector.reset_input_buffer()
    Lector.close()
    Lector = serial.Serial('/dev/ttyACM0', 9600)
    AutoAOD = Automatico("AOD",AOD,1)
    AutoAOD.start()
    AutoNFC = Automatico("NFC",NFC,3)
    AutoNFC.start()
    app.run(host=ip_page, port=80)
