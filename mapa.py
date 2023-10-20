import folium
from folium.plugins import Search, Fullscreen
import branca
import apis
import json
import pandas
import shutil

class Mapa:
    def __init__(self):
        shutil.copyfile('templates/indicatorsBase.json', 'templates/indicators.json')
        shutil.copyfile('templates/extraIndicatorsBase.json', 'templates/extraIndicators.json')
        self.indicators = self.__cargarIndicadores()
        geojson_f = open('geodata/municipios.geojson')
        self.geojson = json.load(geojson_f)
        self.__cargarGeoJson()

    def generarMapa(self, filtros, añosInd, colormapInd, fechaIncidencia):
        mapa = folium.Map(tiles="cartodb positron")
        geojson_fields = ['iz_ofizial']
        geojson_aliases = ['Municipio:']
        # Indicadores y colormap
        self.__generarIndicadoresColormap(mapa, filtros, añosInd, colormapInd, geojson_fields, geojson_aliases)
        # Trafico
        self.__generarEventosTrafico(mapa, filtros, fechaIncidencia)
        # Eventos
        self.__generarEventosGenerales(mapa, filtros)
        # Generar geojson con la informacion y añadir plugins
        geo = folium.GeoJson(
            self.geojson, 
            tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases), 
            name='geojson').add_to(mapa)
        Fullscreen(
            position="topright",
            title="Expandir mapa",
            title_cancel="Salir de pantalla completa",
            force_separate_button=True,
        ).add_to(mapa)
        folium.TileLayer('OpenStreetMap').add_to(mapa)
        folium.LayerControl().add_to(mapa)
        mapa.fit_bounds(mapa.get_bounds())
        Search(layer=geo,
                geom_type='Polygon',
                placeholder='Busca un municipio',
                collapsed=False,
                search_label='iz_ofizial',
                weight=3).add_to(mapa)
        # Generar el mapa y guardarlo
        mapa.save("templates/mapa.html")

    def añadirIndicador(self, indId, indTipo, indName, descInd):
        newInd = {indId: [indTipo, indName, descInd]}
        # Añadir nuevo indicador a indicators.json
        with open('templates/indicators.json', 'r') as fR:
            indicators_raw = fR.read()
            indicators = json.loads(indicators_raw)
            indicators.update(newInd)
        with open('templates/indicators.json', 'w') as fW:
            json.dump(indicators, fW)
        self.indicators[indId] = [indTipo, indName, descInd]
        # Eliminar nuevo indicador de extraIndicators.json
        with open('templates/extraIndicators.json', 'r') as fExtraR:
            extraIndicators_raw = fExtraR.read()
            extraIndicators = json.loads(extraIndicators_raw)
            del extraIndicators[indId]
        with open('templates/extraIndicators.json', 'w') as fExtraW:
            json.dump(extraIndicators, fExtraW)
        # Cargar el nuevo indicador en el geojson
        self.__cargarNuevoIndGeoJson(indId)
    
    def eliminarIndicador(self, indId, indTipo, indName, descInd):
        # Eliminar indicador de indicators.json
        del self.indicators[indId]
        with open('templates/indicators.json', 'w') as fR:
            json.dump(self.indicators, fR)
        # Añadir indicador a extraIndicators.json
        newExtraInd = {indId: [indTipo, indName, descInd]}
        with open('templates/extraIndicators.json', 'r') as fExtraR:
            extraIndicators_raw = fExtraR.read()
            extraIndicators = json.loads(extraIndicators_raw)
            extraIndicators.update(newExtraInd)
        with open('templates/extraIndicators.json', 'w') as fExtraW:
            json.dump(extraIndicators, fExtraW)

    def getAñosInd(self):
        añosInd = {}
        for ind in self.indicators:
            jsonInd = apis.getIndicator(ind)
            años = [list(i['years'][0].keys()) for i in jsonInd['municipalities']]
            añosInd[ind] = años[0]
        return añosInd

    def __cargarGeoJson(self):
        for ind in self.indicators:
            jsonInd = apis.getIndicator(ind)
            for indMun in jsonInd['municipalities']:
                for municipio in self.geojson['features']:
                    if municipio['properties']['ud_kodea'] == indMun['id']:
                        for año in list(indMun['years'][0].keys()):
                            municipio['properties']['indicator_' + str(ind) + '_' + año] = indMun['years'][0][año]

    def __cargarNuevoIndGeoJson(self, ind):
        jsonInd = apis.getIndicator(ind)
        for indMun in jsonInd['municipalities']:
                for municipio in self.geojson['features']:
                    if municipio['properties']['ud_kodea'] == indMun['id']:
                        for año in list(indMun['years'][0].keys()):
                            municipio['properties']['indicator_' + str(ind) + '_' + año] = indMun['years'][0][año]

    def __generarIndicadoresColormap(self, mapa, filtros, añosInd, colormapInd, geojson_fields, geojson_aliases):
        rankingColormapInd = {}
        rankingColormapGeneral = []
        # Indicadores
        for indicator in self.indicators:
            año = añosInd['filtroInd' + str(indicator)]
            if filtros['filtroInd' + str(indicator)]:
                geojson_fields.append('indicator_' + str(indicator) + '_' + año)
                geojson_aliases.append(self.indicators[indicator][1] + ' (' + año + ')')
            # Colormap
            if colormapInd['colormapIndEconomia']:
                if self.indicators[indicator][0] == 'Economía / Competitividad':
                    rankingColormapInd[indicator] = self.__calcularRankingInd(indicator)
                    rankingColormapGeneral = self.__actualizarRankingGeneral(rankingColormapGeneral, rankingColormapInd[indicator])
            elif colormapInd['colormapIndCohesion']:
                if self.indicators[indicator][0] == 'Cohesión social / Calidad de vida':
                    rankingColormapInd[indicator] = self.__calcularRankingInd(indicator)
                    rankingColormapGeneral = self.__actualizarRankingGeneral(rankingColormapGeneral, rankingColormapInd[indicator])
            elif colormapInd['colormapIndMedioambiente']:
                if self.indicators[indicator][0] == 'Medioambiente y Movilidad':
                    rankingColormapInd[indicator] = self.__calcularRankingInd(indicator)
                    rankingColormapGeneral = self.__actualizarRankingGeneral(rankingColormapGeneral, rankingColormapInd[indicator])
            elif colormapInd['colormapInd' + str(indicator)]:
                ind_colormap = indicator
                año_colormap = año
                jsonInd = apis.getIndicator(indicator)
                data = {'lugar': [], 'dato': []}
                for indMunicipio in jsonInd['municipalities']:
                    if año_colormap in indMunicipio['years'][0]:
                        data['lugar'].append(indMunicipio['name'])
                        data['dato'].append(indMunicipio['years'][0][año_colormap])
                df = pandas.DataFrame(data)
                # Se define el verde como color para los valores más altos.
                myColors = ['red', 'orange','yellow', 'green']
                # Si un numero mas alto es negativo se escoge el rojo para los valores altos.
                if not self.indicators[indicator][2]:
                    myColors = ['green', 'yellow','orange', 'red']
                colormap = branca.colormap.LinearColormap(
                        colors=myColors,
                        vmin=df.min()['dato'],
                        vmax=df.max()['dato'],
                        caption=self.indicators[ind_colormap][1] + ' (' + año_colormap + ')'
                    ).add_to(mapa)
                st_f = lambda x: {'fillColor': colormap(int(x['properties']['indicator_' + str(ind_colormap) + '_' + año_colormap])), 'weight': 2, 'fillOpacity': 0.5}   
                folium.GeoJson(self.geojson,
                                style_function=st_f,
                                tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases),
                                name='colormap').add_to(mapa)
        
        # Crear y añadir colormap de los grupos de indicadores
        data = {'lugar': [], 'dato': []}
        if colormapInd['colormapIndEconomia']:
            for mun in rankingColormapGeneral:
                for munGeojson in self.geojson['features']:
                    if munGeojson['properties']['iz_ofizial'] == mun['lugar']:
                        munGeojson['properties']['points'] = mun['points']
                data['lugar'].append(mun['lugar'])
                data['dato'].append(mun['points'])
            df = pandas.DataFrame(data)
            colormap = branca.colormap.LinearColormap(
                        colors=['red', 'orange','yellow', 'green'],
                        vmin=df.min()['dato'],
                        vmax=df.max()['dato'],
                        caption='Puntuación de los indicadores del grupo Economía/Competitividad'
                    ).add_to(mapa)
            st_f = lambda x: {'fillColor': colormap(int(x['properties']['points'])), 'weight': 2, 'fillOpacity': 0.5}
            geojson_fields.append('points')
            geojson_aliases.append('Puntuación del grupo Economía/Competitividad')
                    
            folium.GeoJson(self.geojson,
                            style_function=st_f,
                            tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases),
                            name='colormap').add_to(mapa)
            
        elif colormapInd['colormapIndCohesion']:
            for mun in rankingColormapGeneral:
                for munGeojson in self.geojson['features']:
                    if munGeojson['properties']['iz_ofizial'] == mun['lugar']:
                        munGeojson['properties']['points'] = mun['points']
                data['lugar'].append(mun['lugar'])
                data['dato'].append(mun['points'])
            df = pandas.DataFrame(data)
            colormap = branca.colormap.LinearColormap(
                        colors=['red', 'orange','yellow', 'green'],
                        vmin=df.min()['dato'],
                        vmax=df.max()['dato'],
                        caption='Puntuación de los indicadores del grupo Cohesión social/Calidad de vida'
                    ).add_to(mapa)     
            st_f = lambda x: {'fillColor': colormap(int(x['properties']['points'])), 'weight': 2, 'fillOpacity': 0.5} 
            geojson_fields.append('points')
            geojson_aliases.append('Puntuación del grupo Cohesión social/Calidad de vida')
            folium.GeoJson(self.geojson,
                            style_function=st_f,
                            tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases),
                            name='colormap').add_to(mapa)

        elif colormapInd['colormapIndMedioambiente']:
            for mun in rankingColormapGeneral:
                for munGeojson in self.geojson['features']:
                    if munGeojson['properties']['iz_ofizial'] == mun['lugar']:
                        munGeojson['properties']['points'] = mun['points']
                data['lugar'].append(mun['lugar'])
                data['dato'].append(mun['points'])
            df = pandas.DataFrame(data)
            colormap = branca.colormap.LinearColormap(
                        colors=['red', 'orange','yellow', 'green'],
                        vmin=df.min()['dato'],
                        vmax=df.max()['dato'],
                        caption='Puntuación de los indicadores del grupo Medioambiente y Movilidad'
                    ).add_to(mapa)
            st_f= lambda x: {'fillColor': colormap(int(x['properties']['points'])), 'weight': 2, 'fillOpacity': 0.5}
            geojson_fields.append('points')
            geojson_aliases.append('Puntuación del grupo Medioambiente y Movilidad')
            folium.GeoJson(self.geojson,
                            style_function=st_f,
                            tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases),
                            name='colormap').add_to(mapa)
                   

    def __generarEventosTrafico(self, mapa, filtros, fechaIncidencia):
        myIFrame = None
        myIcon = None
        myPopup = None
        if filtros['filtroTraf1']:
            listaJsonCamaras = apis.getCamaras()
            fg_camaras = folium.FeatureGroup(name="camaras")
            for jsonCamara in listaJsonCamaras:
                for camara in jsonCamara['cameras']:
                    if float(camara['latitude']) < 45 and float(camara['longitude']) < 0:
                        #myIFrame = folium.IFrame('<strong>Latitud:</strong> ' + camara['latitud'] + '<br><br>' + '<strong>Longitud:</strong> ' + camara['longitud'])
                        #myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                        myIcon = folium.Icon(color='red', icon='video-camera', prefix='fa')
                        folium.Marker(location=[camara['latitude'], camara['longitude']], icon = myIcon).add_to(fg_camaras)
            fg_camaras.add_to(mapa)
        if filtros['filtroTraf2']:
            listaJsonIncidencias = apis.getIncidenciasDia(fechaIncidencia)
            fg_incidencias = folium.FeatureGroup(name="incidencias")
            for jsonInc in listaJsonIncidencias:
                for inc in jsonInc['incidences']:
                    if 'endDate' in inc:
                        myIFrame = folium.IFrame(
                            '<strong>Día de inicio:</strong> ' + inc['startDate'].split('T')[0] + '<br><br><strong>Hora de inicio:</strong> ' +
                            inc['startDate'].split('T')[1] + '<br><br><strong>Día de fin:</strong> ' + inc['endDate'].split('T')[0] + 
                            '<br><br><strong>Hora de fin:</strong> ' + inc['endDate'].split('T')[1] + '<br><br><strong>Tipo:</strong> ' + 
                            inc['incidenceType'] + '<br><br><strong>Causa:</strong> ' + inc['cause'])
                    else:
                        myIFrame = folium.IFrame(
                            '<strong>Día:</strong> ' + inc['startDate'].split('T')[0] + '<br><br><strong>Hora:</strong> ' +
                            inc['startDate'].split('T')[1] + '<br><br><strong>Tipo:</strong> ' + inc['incidenceType'] + 
                            '<br><br><strong>Causa:</strong> ' + inc['cause'])
                    myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                    myIcon = folium.Icon(color='red', icon='car', prefix='fa')
                    folium.Marker(location=[inc['latitude'], inc['longitude']],popup = myPopup, icon = myIcon).add_to(fg_incidencias)
            fg_incidencias.add_to(mapa)

    def __generarEventosGenerales(self, mapa, filtros):
        if filtros['filtroEv2'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosConcierto()
            fg_conciertos = folium.FeatureGroup(name='conciertos')
            self.__añadirEventos(jsonEventos, fg_conciertos)
            fg_conciertos.add_to(mapa)
        if filtros['filtroEv3'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosTeatro()
            fg_teatros = folium.FeatureGroup(name='teatros')
            self.__añadirEventos(jsonEventos, fg_teatros)
            fg_teatros.add_to(mapa)
        if filtros['filtroEv4'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosDanza()
            fg_danzas = folium.FeatureGroup(name='danzas')
            self.__añadirEventos(jsonEventos, fg_danzas)
            fg_danzas.add_to(mapa)
        if filtros['filtroEv5'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosConferencia()
            fg_conferencias = folium.FeatureGroup(name='conferencias')
            self.__añadirEventos(jsonEventos, fg_conferencias)
            fg_conferencias.add_to(mapa)
        if filtros['filtroEv6'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosBertsolaritza()
            fg_bertsolaritza = folium.FeatureGroup(name='bertsolaritza')
            self.__añadirEventos(jsonEventos, fg_bertsolaritza)
            fg_bertsolaritza.add_to(mapa)
        if filtros['filtroEv7'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosFeria()
            fg_ferias = folium.FeatureGroup(name='ferias')
            self.__añadirEventos(jsonEventos, fg_ferias)
            fg_ferias.add_to(mapa)
        if filtros['filtroEv8'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosExposicion()
            fg_exposiciones = folium.FeatureGroup(name='exposiciones')
            self.__añadirEventos(jsonEventos, fg_exposiciones)
            fg_exposiciones.add_to(mapa)
        if filtros['filtroEv9'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosProyeccion()
            fg_proyecciones = folium.FeatureGroup(name='proyecciones')
            self.__añadirEventos(jsonEventos, fg_proyecciones)
            fg_proyecciones.add_to(mapa)
        if filtros['filtroEv10'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosFormacion()
            fg_formaciones = folium.FeatureGroup(name='formaciones')
            self.__añadirEventos(jsonEventos, fg_formaciones)
            fg_formaciones.add_to(mapa)
        if filtros['filtroEv11'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosConcurso()
            fg_concursos = folium.FeatureGroup(name='concursos')
            self.__añadirEventos(jsonEventos, fg_concursos)
            fg_concursos.add_to(mapa)
        if filtros['filtroEv12'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosFestival()
            fg_festivales = folium.FeatureGroup(name='festivales')
            self.__añadirEventos(jsonEventos, fg_festivales)
            fg_festivales.add_to(mapa)
        if filtros['filtroEv13'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosInfantil()
            fg_infantiles = folium.FeatureGroup(name='infantiles')
            self.__añadirEventos(jsonEventos, fg_infantiles)
            fg_infantiles.add_to(mapa)
        if filtros['filtroEv14'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosFiesta()
            fg_fiestas = folium.FeatureGroup(name='fiestas')
            self.__añadirEventos(jsonEventos, fg_fiestas)
            fg_fiestas.add_to(mapa)
        if filtros['filtroEv15'] or filtros['filtroEv1']:
            jsonEventos = apis.getProximosOtro()
            fg_otros = folium.FeatureGroup(name='otros')
            self.__añadirEventos(jsonEventos, fg_otros)
            fg_otros.add_to(mapa)

    def __añadirEventos(self, jsonEventos, fg):
        myIFrame = None
        myIcon = None
        myPopup = None
        for evento in jsonEventos['items']:
            if self.__esEuskadi(evento['provinceNoraCode']):
                if 'priceEs' in evento:
                    myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nameEs'] + 
                                            '<br><br><strong>Tipo de evento:</strong> ' + evento['typeEs'] + 
                                            '<br><br><strong>Día de inicio:</strong> ' + evento['startDate'].split("T")[0] +
                                            '<br><br><strong>Hora de inicio:</strong> ' + evento['startDate'].split("T")[1][:-1] + 
                                            '<br><br><strong>Día de fin:</strong> ' + evento['endDate'].split("T")[0] +
                                            '<br><br><strong>Hora de fin:</strong> ' + evento['endDate'].split("T")[1][:-1] +
                                            '<br><br><strong>Precio:</strong> ' + evento['priceEs'])
                else:
                    myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nameEs'] + 
                                            '<br><br><strong>Tipo de evento:</strong> ' + evento['typeEs'] + 
                                            '<br><br><strong>Día de inicio:</strong> ' + evento['startDate'].split("T")[0] +
                                            '<br><br><strong>Hora de inicio:</strong> ' + evento['startDate'].split("T")[1][:-1] + 
                                            '<br><br><strong>Día de fin:</strong> ' + evento['endDate'].split("T")[0] +
                                            '<br><br><strong>Hora de fin:</strong> ' + evento['endDate'].split("T")[1][:-1] +
                                            '<br><br><strong>Precio:</strong> Sin información')
                myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                myIcon = self.__getIconoEvento(evento)
                folium.Marker(location=[evento['municipalityLatitude'], evento['municipalityLongitude']], popup = myPopup, icon = myIcon).add_to(fg)
        
    def __esEuskadi(self, provinciaCod):
        if provinciaCod == '48' or provinciaCod == '20' or provinciaCod == '1':
            return True
        else:
            return False

    def __actualizarRankingGeneral(self, rankingGeneral, rankingInd):
        points = len(rankingInd)
        if len(rankingGeneral) <= 0:
            for munInd in rankingInd:
                tmpDict = {'lugar': munInd['lugar'], 'points': points}
                rankingGeneral.append(tmpDict)
                points = points - 1
        else:
            for munInd in rankingInd:
                for munGen in rankingGeneral:
                    if munInd['lugar'] == munGen['lugar']:
                        munGen['points'] = munGen['points'] + points
                        points = points - 1   
        return rankingGeneral

    def __calcularRankingInd(self, indicator):
        rankingInd = []
        jsonInd = apis.getIndicator(indicator)
        if self.indicators[indicator][2]:
            for ind in jsonInd['municipalities']:
                tmp_dict = {'lugar': ind['name'], 'data': ind['years'][0][list(ind['years'][0])[-1]]}
                self.__reverse_insort(rankingInd, tmp_dict)
        else:
            for ind in jsonInd['municipalities']:
                tmp_dict = {'lugar': ind['name'], 'data': ind['years'][0][list(ind['years'][0])[-1]]}
                self.__insort(rankingInd, tmp_dict)
        return rankingInd

    def __reverse_insort(self, a, x):
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo+hi)//2
            if x['data'] > a[mid]['data']:
                hi = mid
            else:
                lo = mid+1
        a.insert(lo, x)

    def __insort(self, a, x):
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo+hi)//2
            if x['data'] < a[mid]['data']:
                hi = mid
            else:
                lo = mid+1
        a.insert(lo, x)
    
    def __getIconoEvento(self, evento):
        myIcon = folium.Icon(color='green', icon='question', prefix='fa')
        if evento['type'] == 1: #concierto
            myIcon = folium.Icon(color='green', icon='music', prefix='fa')
        if evento['type'] == 2: #teatro
            myIcon = folium.Icon(color='green', icon='film', prefix='fa')
        if evento['type'] == 4: #danza
            myIcon = folium.Icon(color='green', icon='female', prefix='fa')
        if evento['type'] == 6: #conferencia
            myIcon = folium.Icon(color='green', icon='bar-chart', prefix='fa')
        if evento['type'] == 7: #bertsolaritza
            myIcon = folium.Icon(color='green', icon='microphone', prefix='fa')
        if evento['type'] == 8: #feria
            myIcon = folium.Icon(color='green', icon='balance-scale', prefix='fa')
        if evento['type'] == 9 or evento['type'] == 3: #exposicion o proyeccion audiovisual
            myIcon = folium.Icon(color='green', icon='play', prefix='fa')
        if evento['type'] == 11: #formacion
            myIcon = folium.Icon(color='green', icon='graduation-cap', prefix='fa')
        if evento['type'] == 12: #concurso
            myIcon = folium.Icon(color='green', icon='video-camera', prefix='fa')
        if evento['type'] == 13: #festival
            myIcon = folium.Icon(color='green', icon='users', prefix='fa')
        if evento['type'] == 14: #actividad infantil
            myIcon = folium.Icon(color='green', icon='child', prefix='fa')
        if evento['type'] == 15: #otro
            myIcon = folium.Icon(color='green', icon='question', prefix='fa')
        if evento['type'] == 16: #fiestas
            myIcon = folium.Icon(color='green', icon='flag', prefix='fa')
        return myIcon
    
    def __cargarIndicadores(self):
        with open('templates/indicators.json') as f:
            indicators_raw = f.read()
        return json.loads(indicators_raw)

