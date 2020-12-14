from movements import app
from flask import render_template, request, url_for, redirect
import csv
import sqlite3

DBFILE = 'movements/data/basededatos.db'

def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    conn.commit()
    filas = c.fetchall()
    conn.close()


    if len(filas) == 0:
        return filas

# Esto podríamos hacerlo en otra función (anidada). ¿Probarlo? 
    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

@app.route('/')
def listaIngresos():

    ingresos = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos;') or []
    total=0
    for ingreso in ingresos:
        total += float(ingreso['cantidad'])
    
    return render_template('movementsList.html', datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    if request.method == 'POST':
        consulta('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?, ?, ?);', 
                (float(request.form.get('cantidad')), 
                request.form.get('concepto'), 
                request.form.get('fecha')
                )
            )

        return redirect(url_for('listaIngresos'))

    return render_template('alta.html')

@app.route('/modifica/<id>', methods=['GET', 'POST'])
def modificaIngreso(id):
    if request.method == 'GET':
        registro = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos where id = ?', (id,))

        return render_template('modifica.html', registro=registro)
    
    else:
        consulta=('UPDATE movimientos SET fecha = ?, concepto = ?, cantidad = ? WHERE id = ?',
            (request.form.get('fecha'),
            request.form.get('concepto'),
            float(request.form.get('cantidad')),
            id
            )
        )

        return redirect(url_for('listaIngresos'))