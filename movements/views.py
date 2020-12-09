from movements import app
from flask import render_template, request, url_for, redirect
import csv

@app.route('/')
def listaIngresos():
    fIngresos = open("movements/data/basededatos.csv", "r")
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos = list(csvReader)
    total=0
    for ingreso in ingresos:
        total += float(ingreso[2])

    #print(ingresos)
    
    return render_template('movementsList.html', datos=ingresos, total=total)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    if request.method == 'POST':
        fIngresos = open("movements/data/basededatos.csv", "a", newline="")
        csvWriter = csv.writer(fIngresos, delimiter=",", quotechar='"')
        csvWriter.writerow([request.form.get('fecha'), request.form.get('concepto'), request.form.get('cantidad')])
        return redirect(url_for('listaIngresos'))

    return render_template('alta.html')