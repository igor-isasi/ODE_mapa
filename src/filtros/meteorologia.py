from apis import apiMeteo as api
import folium
import json
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def generarPrediccionMeteo(mapa, filtros, fechaMeteo, ubiMeteo, fechaMeteoUbi):
    errorApi = None
    errorGeopy = None
    if filtros['filtroMetPred']:
        fg_predicciones = folium.FeatureGroup(name='predicciones meteorológicas')
        with open('templates/ubiMeteoPrincipales.json') as f:
            ubicaciones_raw = f.read()
            ubicacionesJson = json.loads(ubicaciones_raw)
        for zoneJson in ubicacionesJson['zones']:
            for location in zoneJson['locations']:
                jsonPrediccion = api.getPrediccionSemanal(zoneJson['zone'], location, fechaMeteo)
                if jsonPrediccion != None:
                    errorGeopy = añadirPrediccion(jsonPrediccion, fg_predicciones, location, fechaMeteo)
                else:
                    errorApi = "API de Euskalmet"
        fg_predicciones.add_to(mapa)
    if filtros['filtroMetPredUbi']:
        fg_predicciones = folium.FeatureGroup(name='prediccion meteorológica por ubicación')
        with open('templates/ubiMeteoTodas.json') as f:
            ubicaciones_raw = f.read()
            ubicacionesJson = json.loads(ubicaciones_raw)
        zone = ubicacionesJson[ubiMeteo]
        jsonPrediccion = api.getPrediccionSemanal(zone, ubiMeteo, fechaMeteoUbi)
        if jsonPrediccion != None:
            errorGeopy = añadirPrediccion(jsonPrediccion, fg_predicciones, ubiMeteo, fechaMeteoUbi)
        else:
            errorApi = "API de Euskalmet"
        fg_predicciones.add_to(mapa)
    return errorApi, errorGeopy

def añadirPrediccion(jsonPrediccion, fg, location, fechaMeteo):
    for diaPred in jsonPrediccion['trendsByDate']['set']:
        fechaPred = diaPred['date'].split('T')[0]
        if fechaPred == fechaMeteo:
            fecha = datetime.strptime(diaPred['date'].split('T')[0], "%Y-%m-%d").strftime('%d-%m-%Y')
            myIFrame = folium.IFrame('<font color="orange">PREDICCIÓN METEOROLÓGICA</font>' + 
                                     '<br><br><strong>Ubicación:</strong> ' + location.capitalize() + 
                                     '<br><br><strong>Fecha:</strong> ' + fecha + 
                                     '<br><br><strong>Resumen:</strong> ' + diaPred['weather']['nameByLang']['SPANISH'] +
                                     '<br><br><strong>Descripción:</strong> ' + diaPred['weather']['descriptionByLang']['SPANISH'] + 
                                     '<br><br><strong>Temperatura mínima:</strong> ' + str(diaPred['temperatureRange']['min']) + ' °C' +  
                                     '<br><br><strong>Temperatura máxima:</strong> ' + str(diaPred['temperatureRange']['max']) + ' °C')
            myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
            myIcon = folium.features.CustomIcon('https://api.euskadi.eus/' + diaPred['weather']['path'], icon_size=(50,50))
            getLoc = do_geocode(location)
            if getLoc != None and getLoc.latitude < 45 and getLoc.latitude > 42 and getLoc.longitude < 0:
                folium.Marker(location=[getLoc.latitude, getLoc.longitude], popup = myPopup, icon = myIcon).add_to(fg)
            else:
                return "No se han podido obtener las coordenadas de alguna(s) ubicación(es) seleccionada(s) para las predicciones meteorológicas."

def do_geocode(address, attempt=1, max_attempts=5):
    try:
        loc = Nominatim(user_agent="Geopy Library")
        return loc.geocode(address)
    except (GeocoderTimedOut, GeocoderUnavailable):
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt+1)
        else:
            return None