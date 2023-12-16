import folium
from folium.plugins import Search, Fullscreen
from apis import apiIndicadores as apiInd
import json
import shutil, os
from filtros import indicadores, trafico, eventos, entidades, meteorologia

class Mapa:
    def __init__(self):
        """ shutil.copyfile('templates/indicatorsBase.json', 'templates/indicators.json')
        shutil.copyfile('templates/extraIndicatorsBase.json', 'templates/extraIndicators.json') """
        self.indicators = self.__cargarIndicadores('templates/indicatorsBase.json')
        geojson_f = open('geodata/municipios.geojson')
        self.geojson = json.load(geojson_f)
        self.__cargarGeoJson()

    def generarMapa(self, idFichero, filtros, añosInd, fechaIncidencia, fechaMeteo, ubiMeteo, fechaMeteoUbi):
        mapa = folium.Map(tiles="OpenStreetMap")
        geojson_fields = ['iz_ofizial']
        geojson_aliases = ['Municipio:']
        erroresApi = []
        # Indicadores y colormap
        errorApiInd = indicadores.generarIndicadoresColormap(mapa, filtros, añosInd, geojson_fields, geojson_aliases, self.indicators, self.geojson)
        # Trafico
        errorApiTraf = trafico.generarEventosTrafico(mapa, filtros, fechaIncidencia)
        # Eventos
        errorApiEv = eventos.generarEventosGenerales(mapa, filtros)
        # Eventos administrativos
        #errorApiEvAd = eventosAdmin.generarEventosAdmin(mapa, filtros, fechaEventosAdmin)
        # Entidades
        errorApiEnt = entidades.generarEntidades(mapa, filtros)
        # Meteorologia
        errorApiMet = meteorologia.generarPrediccionMeteo(mapa, filtros, fechaMeteo, ubiMeteo, fechaMeteoUbi)
        # Comprobar si ha habido error con las APIs en cualquiera de las solicitudes
        if errorApiInd != None:
            erroresApi.append(errorApiInd)
        if errorApiTraf != None:
            erroresApi.append(errorApiTraf)
        if errorApiEv != None:
            erroresApi.append(errorApiEv)
        if errorApiEnt != None:
            erroresApi.append(errorApiEnt)
        if errorApiMet != None:
            erroresApi.append(errorApiMet)
        # Generar geojson con la informacion y añadir plugins
        geo = folium.GeoJson(
            self.geojson, 
            tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases), 
            highlight_function=lambda x: {'fillColor': 'black'},
            name='geojson').add_to(mapa)
        Fullscreen(
            position="topright",
            title="Expandir mapa",
            title_cancel="Salir de pantalla completa",
            force_separate_button=True,
        ).add_to(mapa)
        folium.TileLayer('cartodb positron').add_to(mapa)
        folium.LayerControl().add_to(mapa)
        mapa.fit_bounds(mapa.get_bounds(), padding = (1,1))
        Search(layer=geo,
                geom_type='Polygon',
                placeholder='Busca un municipio',
                collapsed=False,
                search_label='iz_ofizial',
                weight=3).add_to(mapa)
        # Generar el mapa y guardarlo
        mapa.save("templates/mapa.html")
        return erroresApi

    def añadirIndicador(self, idFichero, indId, indTipo, indName, descInd):
        rutaFichero = 'templates/session_templates/indicators' + str(idFichero) + '.json'
        rutaFicheroExtra = 'templates/session_templates/extraIndicators' + str(idFichero) + '.json'
        # Si todavía no existen ficheros para esta sesión crearlos a partir de los base
        if not os.path.exists(rutaFichero):
            shutil.copyfile('templates/indicatorsBase.json', rutaFichero)
        if not os.path.exists(rutaFicheroExtra):
            shutil.copyfile('templates/extraIndicatorsBase.json', rutaFicheroExtra)
        newInd = {indId: [indTipo, indName, descInd]}
        # Añadir nuevo indicador a indicators.json
        with open(rutaFichero, 'r') as fR:
            indicators_raw = fR.read()
            indicators = json.loads(indicators_raw)
            indicators.update(newInd)
        with open(rutaFichero, 'w') as fW:
            json.dump(indicators, fW)
        self.indicators[indId] = [indTipo, indName, descInd]
        # Eliminar nuevo indicador de extraIndicators.json
        with open(rutaFicheroExtra, 'r') as fExtraR:
            extraIndicators_raw = fExtraR.read()
            extraIndicators = json.loads(extraIndicators_raw)
            del extraIndicators[indId]
        with open(rutaFicheroExtra, 'w') as fExtraW:
            json.dump(extraIndicators, fExtraW)
        # Cargar el nuevo indicador en el geojson
        return(self.__cargarNuevoIndGeoJson(indId))
    
    def eliminarIndicador(self, idFichero, indId, indTipo, indName, descInd):
        rutaFichero = 'templates/session_templates/indicators' + str(idFichero) + '.json'
        rutaFicheroExtra = 'templates/session_templates/extraIndicators' + str(idFichero) + '.json'
         # Si todavía no existen ficheros para esta sesión crearlos a partir de los base
        if not os.path.exists(rutaFichero):
            shutil.copyfile('templates/indicatorsBase.json', rutaFichero)
        if not os.path.exists(rutaFicheroExtra):
            shutil.copyfile('templates/extraIndicatorsBase.json', rutaFicheroExtra)
        # Eliminar indicador de indicators.json
        del self.indicators[indId]
        with open(rutaFichero, 'w') as fR:
            json.dump(self.indicators, fR)
        # Añadir indicador a extraIndicators.json
        newExtraInd = {indId: [indTipo, indName, descInd]}
        with open(rutaFicheroExtra, 'r') as fExtraR:
            extraIndicators_raw = fExtraR.read()
            extraIndicators = json.loads(extraIndicators_raw)
            extraIndicators.update(newExtraInd)
        with open(rutaFicheroExtra, 'w') as fExtraW:
            json.dump(extraIndicators, fExtraW)
        
    def reiniciarIndicadores(self, idFichero):
        rutaFichero = 'templates/session_templates/indicators' + str(idFichero) + '.json'
        rutaFicheroExtra = 'templates/session_templates/extraIndicators' + str(idFichero) + '.json'
         # Si todavía no existen ficheros para esta sesión crearlos a partir de los base
        if not os.path.exists(rutaFichero):
            shutil.copyfile('templates/indicatorsBase.json', rutaFichero)
        if not os.path.exists(rutaFicheroExtra):
            shutil.copyfile('templates/extraIndicatorsBase.json', rutaFicheroExtra)
        shutil.copyfile('templates/indicatorsBase.json', rutaFichero)
        shutil.copyfile('templates/extraIndicatorsBase.json', rutaFicheroExtra)
        self.indicators = self.__cargarIndicadores(rutaFichero)

    def getAñosInd(self):
        añosInd = {}
        for ind in self.indicators:
            jsonInd = apiInd.getIndicator(ind)
            if jsonInd != None:
                años = [list(i['years'][0].keys()) for i in jsonInd['municipalities']]
                añosInd[ind] = años[0]
            else:
                añosInd = None
                break
        return añosInd

    def __cargarGeoJson(self):
        errorApi = False
        for ind in self.indicators:
            jsonInd = apiInd.getIndicator(ind)
            if jsonInd != None:
                for indMun in jsonInd['municipalities']:
                    for municipio in self.geojson['features']:
                        if municipio['properties']['ud_kodea'] == indMun['id']:
                            for año in list(indMun['years'][0].keys()):
                                municipio['properties']['indicator_' + str(ind) + '_' + año] = indMun['years'][0][año]
            else:
                errorApi = True
                break
        return errorApi
                
    def __cargarNuevoIndGeoJson(self, ind):
        jsonInd = apiInd.getIndicator(ind)
        errorApi = False
        if jsonInd != None:
            for indMun in jsonInd['municipalities']:
                    for municipio in self.geojson['features']:
                        if municipio['properties']['ud_kodea'] == indMun['id']:
                            for año in list(indMun['years'][0].keys()):
                                municipio['properties']['indicator_' + str(ind) + '_' + año] = indMun['years'][0][año]
        else:
            errorApi = True
        return errorApi
    
    def __cargarIndicadores(self, rutaFichero):
        with open(rutaFichero) as f:
            indicators_raw = f.read()
        return json.loads(indicators_raw)