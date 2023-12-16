from flask import Flask, render_template, request, jsonify, session
from mapa import Mapa
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
idFichero = {}
myMapa = Mapa()

@app.before_request
def before_request():
    if session.get('idFichero') == None:
        session['idFichero'] = uuid.uuid4()
        session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        dataForm = request.form
        tipoRequest = dataForm['tipoRequest']
        if tipoRequest == 'mapa':
            filtros = json.loads(dataForm['filtros'])
            añosInd = json.loads(dataForm['añosInd'])
            fechaIncidencia = dataForm['fechaIncidencia']
            fechaMeteo = dataForm['fechaMeteo']
            ubiMeteo = dataForm['ubiMeteo']
            fechaMeteoUbi = dataForm['fechaMeteoUbi']
            idFichero = session.get('idFichero')
            erroresApi = myMapa.generarMapa(idFichero, filtros, añosInd, fechaIncidencia, fechaMeteo, ubiMeteo, fechaMeteoUbi)
            if len(erroresApi) > 0:
                return jsonify(erroresApi)
            return 'mapa cargado'

@app.route('/mapa.html/')
def mapa_html():
    return render_template('mapa.html')

@app.route('/indicators.json/')
def indicators_json():
    idFichero = session.get('idFichero')
    rutaFichero = 'session_templates/indicators' + str(idFichero) + '.json'
    print(rutaFichero, flush=True)
    if os.path.exists('templates/' + rutaFichero):
        print('Existe fichero de sesión. ID: ' + str(idFichero), flush=True)
        return render_template(rutaFichero)
    else:
        print('No existe fichero de sesión', flush=True)
        return render_template('indicatorsBase.json')

@app.route('/extraIndicators.json/')
def extraIndicators_json():
    idFichero = session.get('idFichero')
    rutaFichero = 'session_templates/extraIndicators' + str(idFichero) + '.json'
    if os.path.exists('templates/' + rutaFichero):     
        return render_template(rutaFichero)
    else:
        return render_template('extraIndicatorsBase.json')

@app.route('/webServiceAñosInd/')
def getAñosInd():
    añosInd = myMapa.getAñosInd()
    if añosInd != None:
        return añosInd
    else:
        return 'ApiError'

@app.route('/webServiceAñadirIndicador', methods=['POST'])
def añadirIndicador():
    if request.method == 'POST':
        dataJson = request.get_json()
        indicatorId = dataJson['ind'].split(':')[0]
        tipoInd = dataJson['ind'].split(':')[1]
        nombreInd = dataJson['ind'].split(':')[2]
        descInd = bool(dataJson['ind'].split(':')[3])
        idFichero = session.get('idFichero')
        errorApi = myMapa.añadirIndicador(idFichero, indicatorId, tipoInd, nombreInd, descInd)
        if not errorApi:
            return 'Indicador añadido'
        else:
            return 'ApiError'
    
@app.route('/webServiceEliminarIndicador', methods=['POST'])
def eliminarIndicador():
    if request.method == 'POST':
        dataJson = request.get_json()
        indicatorId = dataJson['ind'].split(':')[0]
        tipoInd = dataJson['ind'].split(':')[1]
        nombreInd = dataJson['ind'].split(':')[2]
        descInd = bool(dataJson['ind'].split(':')[3])
        idFichero = session.get('idFichero')
        myMapa.eliminarIndicador(idFichero, indicatorId, tipoInd, nombreInd, descInd)
        return 'Indicador eliminado'
    
@app.route('/webServiceReiniciarIndicadores')
def reiniciarIndicadores():
    idFichero = session.get('idFichero')
    myMapa.reiniciarIndicadores(idFichero)
    return 'Indicadores reiniciados'
    
@app.route('/ubiMeteoTodas.json/')
def ubiMeteoTodas_json():
    return render_template('ubiMeteoTodas.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
