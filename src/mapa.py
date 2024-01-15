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
        mapa = folium.Map(tiles="OpenStreetMap")
        geojson_fields = ['iz_ofizial']
        geojson_aliases = ['Municipio:']
        indicators = indicadores.cargarIndicadoresSesion(self.idFichero)
        erroresApi = []
        # Indicadores y colormap
        errorApiInd = indicadores.generarIndicadoresColormap(mapa, filtros, añosInd, geojson_fields, geojson_aliases, indicators, self.geojson)
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
        mapa.save("templates/session_maps/mapa" + str(self.idFichero) + ".html")
        return erroresApi

    def __cargarGeoJson(self):
        errorApi = False
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
                errorApi = True
                break
        return errorApi
                
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