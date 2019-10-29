from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import serial, time
import _thread

dias = {0:'Lunes',1:'Martes',2:'Miercoles',3:'Jueves',4:'Viernes',5:'Sabado',6:'Domingo'}
minutos = {0:'00',1:'01',2:'02',3:'03',4:'04',5:'05',6:'06',7:'07',8:'08',9:'09'}

@app.route('/time')
def Time():
    if time.localtime()[4] in minutos:
        hour = str(time.localtime()[3])+":"+minutos.get(time.localtime()[4])
    else:
        hour = str(time.localtime()[3])+":"+str(time.localtime()[4])
    for clase in clase:
        if clase[time.localtime()[6]+2] == hour:
            lab = clase[8]
            Open(lab)
    return ('uwu')

@app.route('/open')
def Open(lab):
    if lab == 'Seleccionar Laboratorio':
        flash('Laboratorio no valido')
        return redirect(url_for('Acciones'))
    acc = serial.Serial(ard.get(lab),9600)
    acc.write('1'.encode())
    acc.close()
    flash('Seguro de %s abrir' % lab)
    return redirect(url_for('Acciones'))

@app.route('/close')
def Close(lab):
    if lab == 'Seleccionar Laboratorio':
        flash('Laboratorio no valido')
        return redirect(url_for('Acciones'))
    acc = serial.Serial(ard.get(lab),9600)
    acc.write('0'.encode())
    acc.close()
    flash('Seguro de %s abrir' % lab)
    return redirect(url_for('Acciones'))
