from movements import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3

@app.route('/')
def listaIngresos():
    conn = sqlite3.connect('movements/data/basededatos.db')
    c = conn.cursor()

    c.execute('SELECT fecha, concepto, cantidad, id FROM movimientos;')


    '''
    fIngresos = open("movements/data/basededatos.csv", "r")
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos = list(csvReader)
    '''
    ingresos = c.fetchall()

    total=0
    for ingreso in ingresos:
        total += float(ingreso[2])
    
    conn.close()

    return render_template('movementsList.html', datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    if request.method == 'POST':
        conn = sqlite3.connect('movements/data/basededatos.db')
        c = conn.cursor()
        
        c.execute('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?, ?, ?);', 
                (float(request.form.get('cantidad')), 
                request.form.get('concepto'), 
                request.form.get('fecha')))
        
        conn.commit()
        conn.close()
        '''
        fIngresos = open("movements/data/basededatos.csv", "a", newline="")
        csvWriter = csv.writer(fIngresos, delimiter=",", quotechar='"')
        csvWriter.writerow([request.form.get('fecha'), request.form.get('concepto'), request.form.get('cantidad')])
        '''
        return redirect(url_for('listaIngresos'))

    return render_template('alta.html')

@app.route('/modifica/<id>', methods=['GET', 'POST'])
def modificaIngreso(id):
    if request.method == 'GET':
        conn = sqlite3.connect('movements/data/basededatos.db')
        c = conn.cursor()

        c.execute('SELECT fecha, concepto, cantidad, id FROM movimientos WHERE id = ?;', id)
        registros = c.fetchall()

        conn.close()

        return render_template('modifica.html', movimiento='id', datos=registros )
    
    if request.method == 'POST':
        conn = sqlite3.connect('movements/data/basededatos.db')
        c = conn.cursor()

        c.execute('UPDATE movimientos SET fecha = ?, concepto = ?, cantidad = ? WHERE id = ?;', 
                (request.form.get('fecha'), 
                request.form.get('concepto'), 
                (float(request.form.get('cantidad'))),
                id))
        
        conn.commit()
        conn.close()
    
        return redirect(url_for('listaIngresos'))