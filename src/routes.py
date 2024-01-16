from flask import Blueprint, render_template, request, session, jsonify
from mapa import Mapa
from filtros import indicadores
import uuid, json, os

routes = Blueprint('routes', __name__, template_folder='templates')
mapas = {}

@routes.before_app_request
def before_app_request():
    if session.get('idFichero') == None:
        session['idFichero'] = uuid.uuid4()
        mapas[session.get('idFichero')] = Mapa(session.get('idFichero'))
        print('Se ha añadido mapa: ' + str(mapas), flush=True)
        session.permanent = True

@routes.route('/', methods=['GET', 'POST'])
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
            mapaSesion = mapas[session.get('idFichero')]
            erroresApi = mapaSesion.generarMapa(filtros, añosInd, fechaIncidencia, fechaMeteo, ubiMeteo, fechaMeteoUbi)
            if len(erroresApi) > 0:
                return jsonify(erroresApi)
            return 'mapa cargado'

@routes.route('/mapa.html/')
def mapa_html():
    idFichero = session.get('idFichero')
    rutaFichero = 'session_maps/mapa' + str(idFichero) + '.html'
    print(rutaFichero, flush=True)
    if os.path.exists('templates/' + rutaFichero):
        return render_template(rutaFichero)
    else:
        return render_template('mapa.html')

@routes.route('/indicators.json/')
def indicators_json():
    idFichero = session.get('idFichero')
    rutaFichero = 'session_indicators/indicators' + str(idFichero) + '.json'
    print(rutaFichero, flush=True)
    if os.path.exists('templates/' + rutaFichero):
        print('Existe fichero de sesión. ID: ' + str(idFichero), flush=True)
        return render_template(rutaFichero)
    else:
        print('No existe fichero de sesión', flush=True)
        return render_template('indicatorsBase.json')

@routes.route('/extraIndicators.json/')
def extraIndicators_json():
    idFichero = session.get('idFichero')
    rutaFichero = 'session_indicators/extraIndicators' + str(idFichero) + '.json'
    if os.path.exists('templates/' + rutaFichero):     
        return render_template(rutaFichero)
    else:
        return render_template('extraIndicatorsBase.json')
    
@routes.route('/ubiMeteoTodas.json/')
def ubiMeteoTodas_json():
    return render_template('ubiMeteoTodas.json')

@routes.route('/webServiceAñosInd/')
def getAñosInd():
    idFichero = session.get('idFichero')
    añosInd = indicadores.getAñosIndSesion(idFichero)
    if añosInd != None:
        return añosInd
    else:
        return 'ApiError'

@routes.route('/webServiceAñadirIndicador', methods=['POST'])
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
    
@routes.route('/webServiceEliminarIndicador', methods=['POST'])
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
    
@routes.route('/webServiceReiniciarIndicadores')
def reiniciarIndicadores():
    idFichero = session.get('idFichero')
    indicadores.reiniciarIndicadoresSesion(idFichero)
    return 'Indicadores reiniciados'