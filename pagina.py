from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import serial
import MySQLdb as sqlnoflask

# Configuracion inical
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2469'
app.config['MYSQL_DB'] = 'Horario'
app.secret_key = 'UwU'
mysql = MySQL(app)
noflask = sqlnoflask.connect('localhost','root','2469','Horario')

# Varibles necesarias
ard = {'L1-General': '/dev/ttyACM0', 'L2-Industrial': '/dev/ttyACM0', 'L3-Materiales': '/dev/ttyACM0',
       'L4-Electromedicina': '/dev/ttyACM0', 'L5-Telecomunicaciones': '/dev/ttyACM0', 'L6-Software': '/dev/ttyACM0'}
global laboratorio, laboratorio1, hora, hora1, data
laboratorio = laboratorio1 = hora1 = data = ''

# Revisar horarios
def Automatico():
    print("Automatico")

def AutomaticoA():
    print("Abrir")

def AutomaticoC():
    print ("Cerrar")

# Pagina
@app.route('/')
def main():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM uno')
    data = cur.fetchall()
    cur.close()
    if 'account' in session:
        acc = session['account']
    else:
        acc = ''
    if 'Logged' in session:
        return render_template('abrir.html', user=acc, horarios=data)
    elif 'Edit' in session:
        return render_template('editar.html', user=acc, horarios=data)
    else:
        return render_template('nologin.html', horarios=data)

# Relacionado con la sesion
@app.route('/auth', methods=['POST'])
def Auth():
    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE account = %s AND pass = %s', (user, passw))
        data = cur.fetchone()
        print(data)
        cur.close()
        if data:
            if data[3] == 'Si':
                session['Edit'] = True
                session['account'] = data[1]
                return redirect(url_for('main'))
            session['Logged'] = True
            session['account'] = data[1]
            return redirect(url_for('main'))
        else:
            flash('Usuario o contraseña erroneos')
            return redirect(url_for('main'))
    return redirect(url_for('main'))


@app.route('/logout')
def Logout():
    session.pop('Logged', None)
    session.pop('Edit', None)
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
                flash('Ingrese un laboratorio valido')
                return (redirect(url_for('Editar_Horario')))
        if request.form['lunes'] != "":
            lunes = request.form['lunes']
        else:
            lunes = "No"
        if request.form['martes'] != "":
            martes = request.form['martes']
        else:
            martes = "No"
        if request.form['miercoles'] != "":
            miercoles = request.form['miercoles']
        else:
            miercoles = "No"
        if request.form['jueves'] != "":
            jueves = request.form['jueves']
        else:
            jueves = "No"
        if request.form['viernes'] != "":
            viernes = request.form['viernes']
        else:
            viernes = "No"
        if request.form['sabado'] != "":
            sabado = request.form['sabado']
        else:
            sabado = "No"
        if request.form['clase']:
            clase = request.form['clase']
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO uno (Clase, Lunes, Martes, Miercoles, Jueves, Viernes, Sabado, Laboratorio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
                        (clase, lunes, martes, miercoles, jueves, viernes, sabado, lab))
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
        if lab == 'Laboratorio':
            flash('Laboratorio no valido')
            return redirect(url_for('main'))
        acc = serial.Serial(ard.get(lab), 9600)
        acc.write('1'.encode())
        acc.close()
        flash('Seguro de %s abierto' % lab)
    return redirect(url_for('main'))


@app.route('/cerrar', methods=['POST'])
def Cerrar():
    if request.method == 'POST':
        lab = request.form['laboratorio']
        if lab == 'Laboratorio':
            flash('Laboratorio no valido')
            return redirect(url_for('main'))
        acc = serial.Serial(ard.get(lab), 9600)
        acc.write('0'.encode())
        acc.close()
        flash('Seguro de %s cerrado' % lab)
    return redirect(url_for('main'))


# Iniciar pagina
if __name__ == '__main__':
    app.run(debug=True)
