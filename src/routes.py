from flask import Blueprint, render_template, request, session, jsonify
from mapa import Mapa
from filtros import indicadores
import uuid, json, os

routes = Blueprint('routes', __name__, template_folder='templates')
mapas = {}
erroresGeojson = []

@routes.before_app_request
def before_app_request():
    if session.get('idFichero') == None:
        session['idFichero'] = uuid.uuid4()
        try:
            mapas[session.get('idFichero')] = Mapa(session.get('idFichero'))
        except:
            mapas[session.get('idFichero')] = None
            erroresGeojson.append(session.get('idFichero'))
        session.permanent = True

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if session.get('idFichero') in erroresGeojson:
            return 'ErrorGeojson'
        dataForm = request.form
        tipoRequest = dataForm['tipoRequest']
        if tipoRequest == 'mapa':
            filtros = json.loads(dataForm['filtros'])
            añosInd = json.loads(dataForm['añosInd'])
            fechaIncidencia = dataForm['fechaIncidencia']
            fechaMeteo = dataForm['fechaMeteo']
            ubiMeteo = dataForm['ubiMeteo']
            fechaMeteoUbi = dataForm['fechaMeteoUbi']
            mapaSesion = mapas[session.get('idFichero')]
            errores = mapaSesion.generarMapa(filtros, añosInd, fechaIncidencia, fechaMeteo, ubiMeteo, fechaMeteoUbi)
            if len(errores) > 0:
                return jsonify(errores)
            return 'mapa cargado'

@routes.route('/mapa.html')
def mapa_html():
    mapaSesion = mapas[session.get('idFichero')]
    if mapaSesion != None:
        mapaSesion.mapa.save('templates/mapa.html')
    return render_template('mapa.html')

@routes.route('/indicators.json')
def indicators_json():
    idFichero = session.get('idFichero')
    rutaFichero = 'session_indicators/indicators' + str(idFichero) + '.json'
    if os.path.exists('templates/' + rutaFichero):
        return render_template(rutaFichero)
    else:
        return render_template('indicatorsBase.json')

@routes.route('/extraindicators.json')
def extraIndicators_json():
    idFichero = session.get('idFichero')
    rutaFichero = 'session_indicators/extraIndicators' + str(idFichero) + '.json'
    if os.path.exists('templates/' + rutaFichero):     
        return render_template(rutaFichero)
    else:
        return render_template('extraIndicatorsBase.json')
    
@routes.route('/ubimeteotodas.json')
def ubiMeteoTodas_json():
    return render_template('ubiMeteoTodas.json')

@routes.route('/wsañosind')
def getAñosInd():
    idFichero = session.get('idFichero')
    añosInd = indicadores.getAñosIndSesion(idFichero)
    if añosInd != None:
        return añosInd
    else:
        return 'ApiError'

@routes.route('/wsañadirindicador', methods=['POST'])
def añadirIndicador():
    if request.method == 'POST':
        dataJson = request.get_json()
        indicatorId = dataJson['ind'].split(':')[0]
        tipoInd = dataJson['ind'].split(':')[1]
        nombreInd = dataJson['ind'].split(':')[2]
        descInd = bool(dataJson['ind'].split(':')[3])
        idFichero = session.get('idFichero')
        indicadores.añadirIndicadorSesion(idFichero, indicatorId, tipoInd, nombreInd, descInd)
        errorApi = mapas[idFichero].cargarNuevoIndGeoJson(indicatorId)
        if not errorApi:
            return 'Indicador añadido'
        else:
            return 'ApiError'
    
@routes.route('/wseliminarindicador', methods=['POST'])
def eliminarIndicador():
    if request.method == 'POST':
        dataJson = request.get_json()
        indicatorId = dataJson['ind'].split(':')[0]
        tipoInd = dataJson['ind'].split(':')[1]
        nombreInd = dataJson['ind'].split(':')[2]
        descInd = bool(dataJson['ind'].split(':')[3])
        idFichero = session.get('idFichero')
        indicadores.eliminarIndicadorSesion(idFichero, indicatorId, tipoInd, nombreInd, descInd)
        return 'Indicador eliminado'
    
@routes.route('/wsreiniciarindicadores')
def reiniciarIndicadores():
    idFichero = session.get('idFichero')
    indicadores.reiniciarIndicadoresSesion(idFichero)
    return 'Indicadores reiniciados'