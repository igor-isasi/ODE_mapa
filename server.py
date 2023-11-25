from flask import Flask, render_template, request, jsonify
from mapa import Mapa
import json

app = Flask(__name__)
myMapa = Mapa()

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
            erroresApi = myMapa.generarMapa(filtros, añosInd, fechaIncidencia, fechaMeteo, ubiMeteo, fechaMeteoUbi)
            if len(erroresApi) > 0:
                return jsonify(erroresApi)
            return 'mapa cargado'

@app.route('/mapa.html/')
def mapa_html():
    return render_template('mapa.html')

@app.route('/indicators.json/')
def indicators_json():
    return render_template('indicators.json')

@app.route('/extraIndicators.json/')
def extraIndicators_json():
    return render_template('extraIndicators.json')

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
        errorApi = myMapa.añadirIndicador(indicatorId, tipoInd, nombreInd, descInd)
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
        myMapa.eliminarIndicador(indicatorId, tipoInd, nombreInd, descInd)
        return 'Indicador eliminado'
    
@app.route('/webServiceReiniciarIndicadores')
def reiniciarIndicadores():
    myMapa.reiniciarIndicadores()
    return 'Indicadores reiniciados'
    
@app.route('/ubiMeteoTodas.json/')
def ubiMeteoTodas_json():
    return render_template('ubiMeteoTodas.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
