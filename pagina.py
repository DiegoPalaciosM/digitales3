from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import Acciones, sys

# Configuracion inical
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2469'
app.config['MYSQL_DB'] = 'Horario'
app.secret_key = 'UwU'
mysql = MySQL(app)
ip = sys.argv[1]
# Direcctorio laboratorio

dion = {'L1-General':'1','L2-Industrial':'2','L3-Materiales':'3','L4-Electromedicina':'4','L5-Telecomunicaciones':'5','L6-Software':'6'}
dioff = {'L1-General':'a','L2-Industrial':'b','L3-Materiales':'c','L4-Electromedicina':'d','L5-Telecomunicaciones':'e','L6-Software':'f'}

# Pagina
@app.route('/')
def main():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM uno')
    data = cur.fetchall()
    cur.close()
    if 'account' in session:
        acc = session['account'].title()
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
        cur.execute('SELECT * FROM users WHERE user = %s AND pass = %s', (user, passw))
        data = cur.fetchone()
        mysql.connection.commit()
        if data:
            if data[5] == 'Si':
                session['Edit'] = True
                session['account'] = data[3]
                return redirect(url_for('main'))
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
                print ("aqui"+str(x))
                break
            else:
                existe = 0
        if existe:
            flash('Usuario ya existente')
            return redirect(url_for('main'))
        else:
            if cfpassw == passw and user != "" and nombre != "" and apellido != "":
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (user, pass, nombre, apellido) VALUES ('%s', '%s', '%s', '%s');" % (user, passw, nombre, apellido))
                mysql.connection.commit()
                flash('Usuario registrado')
                return redirect(url_for('main'))
    flash('Error en el formulario de registro')
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
        Acciones.TCP(mensaje,ip)
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
        Acciones.TCP(mensaje,ip)
        flash('Seguro de %s cerrado' % (lab))
    return redirect(url_for('main'))

#Test
@app.route('/test')
def TEST():
    return render_template('separadas/registro-acciones.html')


# Iniciar pagina
if __name__ == '__main__':
    #app.run(host='172.17.92.98',port=80,debug=True) # AI_LAB
    app.run(debug=True) # Localhost
    #app.run(host='10.147.17.207', port=80, debug=True) #ZeroTier
    #app.run(host='192.168.0.4',port=80,debug=True) #Wifi
    #app.run(host='192.168.0.9',port=80,debug=True) #Lan
