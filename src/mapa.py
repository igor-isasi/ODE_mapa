import folium
from folium.plugins import Search, Fullscreen
from apis import apiIndicadores as apiInd
import json
from filtros import indicadores, trafico, eventos, entidades, meteorologia

class Mapa:
    def __init__(self, idFichero):
        self.idFichero = idFichero
        geojson_f = open('geodata/municipios.geojson')
        self.geojson = json.load(geojson_f)
        self.__cargarGeoJson()

    def generarMapa(self, filtros, añosInd, fechaIncidencia, fechaMeteo, ubiMeteo, fechaMeteoUbi):
        self.mapa = folium.Map(tiles="OpenStreetMap")
        geojson_fields = ['iz_ofizial']
        geojson_aliases = ['Municipio:']
        indicators = indicadores.cargarIndicadoresSesion(self.idFichero)
        errores = []
        # Indicadores y colormap
        errorApiInd = indicadores.generarIndicadoresColormap(self.mapa, filtros, añosInd, geojson_fields, geojson_aliases, indicators, self.geojson)
        # Trafico
        errorApiTraf = trafico.generarEventosTrafico(self.mapa, filtros, fechaIncidencia)
        # Eventos
        errorApiEv = eventos.generarEventosGenerales(self.mapa, filtros)
        # Entidades
        errorApiEnt, errorPyproj = entidades.generarEntidades(self.mapa, filtros)
        # Meteorologia
        errorApiMet, errorGeopy = meteorologia.generarPrediccionMeteo(self.mapa, filtros, fechaMeteo, ubiMeteo, fechaMeteoUbi)
        # Comprobar si ha habido error con las APIs en cualquiera de las solicitudes
        if errorApiInd != None:
            errores.append(errorApiInd)
        if errorApiTraf != None:
            errores.append(errorApiTraf)
        if errorApiEv != None:
            errores.append(errorApiEv)
        if errorApiEnt != None:
            errores.append(errorApiEnt)
        if errorApiMet != None:
            errores.append(errorApiMet)
        if errorGeopy != None:
            errores.append(errorGeopy)
        if errorPyproj != None:
            errores.append(errorPyproj)
        # Generar geojson con la informacion y añadir plugins
        geo = folium.GeoJson(
            self.geojson, 
            tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases), 
            highlight_function=lambda x: {'fillColor': 'black'},
            name='geojson').add_to(self.mapa)
        Fullscreen(
            position="topright",
            title="Expandir mapa",
            title_cancel="Salir de pantalla completa",
            force_separate_button=True,
        ).add_to(self.mapa)
        folium.TileLayer('cartodb positron').add_to(self.mapa)
        folium.LayerControl().add_to(self.mapa)
        self.mapa.fit_bounds(self.mapa.get_bounds(), padding = (1,1))
        Search(layer=geo,
                geom_type='Polygon',
                placeholder='Busca un municipio',
                collapsed=False,
                search_label='iz_ofizial',
                weight=3).add_to(self.mapa)
        return errores

    def __cargarGeoJson(self):
        indicators = indicadores.cargarIndicadoresSesion(self.idFichero)
        for ind in indicators:
            jsonInd = apiInd.getIndicator(ind)
            if jsonInd != None:
                for indMun in jsonInd['municipalities']:
                    for municipio in self.geojson['features']:
                        if municipio['properties']['ud_kodea'] == indMun['id']:
                            for año in list(indMun['years'][0].keys()):
                                municipio['properties']['indicator_' + str(ind) + '_' + año] = indMun['years'][0][año]
            else:
                raise

    def cargarNuevoIndGeoJson(self, ind):
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