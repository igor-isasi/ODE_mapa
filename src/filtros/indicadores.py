from apis import apiIndicadores as api
import folium, branca, pandas, os, json, shutil

def generarIndicadoresColormap(mapa, filtros, añosInd, geojson_fields, geojson_aliases, indicators, geojson):
    rankingColormapInd = {}
    rankingColormapGeneral = []
    errorColormapEco = False
    errorColormapCohe = False
    errorColormapMedi = False
    errorColormapInd = False
    errorApi = None
    # Indicadores
    for indicator in indicators:
        año = añosInd['añoFiltroInd' + str(indicator)]
        if filtros['filtroInd' + str(indicator)]:
            geojson_fields.append('indicator_' + str(indicator) + '_' + año)
            geojson_aliases.append(indicators[indicator][1] + ' (' + año + ')')
        # Colormap
        if filtros['colormapIndEconomia']:
            if indicators[indicator][0] == 'Economía / Competitividad':
                jsonInd = api.getIndicator(indicator)
                if jsonInd != None and not errorColormapEco:
                    rankingColormapInd[indicator] = calcularRankingInd(indicator, jsonInd, indicators)
                    rankingColormapGeneral = actualizarRankingGeneral(rankingColormapGeneral, rankingColormapInd[indicator])
                else:
                    if not errorColormapEco:
                        errorApi = 'API de indicadores municipales'
                    errorColormapEco = True
        elif filtros['colormapIndCohesion']:
            if indicators[indicator][0] == 'Cohesión social / Calidad de vida':
                jsonInd = api.getIndicator(indicator)
                if jsonInd != None and not errorColormapCohe:
                    rankingColormapInd[indicator] = calcularRankingInd(indicator, jsonInd, indicators)
                    rankingColormapGeneral = actualizarRankingGeneral(rankingColormapGeneral, rankingColormapInd[indicator])
                else:
                    if not errorColormapCohe:
                        errorApi = 'API de indicadores municipales'
                    errorColormapCohe = True
        elif filtros['colormapIndMedioambiente']:
            if indicators[indicator][0] == 'Medioambiente y Movilidad':
                jsonInd = api.getIndicator(indicator)
                if jsonInd != None and not errorColormapMedi:
                    rankingColormapInd[indicator] = calcularRankingInd(indicator, jsonInd, indicators)
                    rankingColormapGeneral = actualizarRankingGeneral(rankingColormapGeneral, rankingColormapInd[indicator])
                else:
                    if not errorColormapMedi:
                        errorApi = 'API de indicadores municipales'
                    errorColormapMedi = True
        elif filtros['colormapInd' + str(indicator)]:
            ind_colormap = indicator
            año_colormap = año
            jsonInd = api.getIndicator(indicator)
            if jsonInd != None:
                data = {'lugar': [], 'dato': []}
                for indMunicipio in jsonInd['municipalities']:
                    if año_colormap in indMunicipio['years'][0]:
                        data['lugar'].append(indMunicipio['name'])
                        data['dato'].append(indMunicipio['years'][0][año_colormap])
                df = pandas.DataFrame(data)
                # Se define el verde como color para los valores más altos.
                myColors = ['red', 'orange','yellow', 'green']
                # Si un numero mas alto es negativo se escoge el rojo para los valores altos.
                if not indicators[indicator][2]:
                    myColors = ['green', 'yellow','orange', 'red']
                colormap = branca.colormap.LinearColormap(
                        colors=myColors,
                        vmin=df.min()['dato'],
                        vmax=df.max()['dato'],
                        caption=indicators[ind_colormap][1] + ' (' + año_colormap + ')'
                    ).add_to(mapa)
                def st_f(x):
                    if ('indicator_' + str(ind_colormap) + '_' + año_colormap) in x['properties']:
                        return {'fillColor': colormap(int(x['properties']['indicator_' + str(ind_colormap) + '_' + año_colormap])), 'weight': 2, 'fillOpacity': 0.5}
                    else:
                        return {'fillColor': 'black', 'weight': 2, 'fillOpacity': 0.5}

                folium.GeoJson(geojson,
                                style_function=st_f,
                                tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases),
                                name='colormap').add_to(mapa)
            else:
                if not errorColormapInd:
                    errorApi = 'API de indicadores municipales'
                errorColormapInd = True
    # Crear y añadir colormap de los grupos de indicadores
    if filtros['colormapIndEconomia'] and not errorColormapEco:
        myCaption = 'Puntuación del grupo Economía/Competitividad'
        generarColormapGrupo(mapa, rankingColormapGeneral, myCaption, geojson_fields, geojson_aliases, geojson)          
    elif filtros['colormapIndCohesion'] and not errorColormapCohe:
        myCaption = 'Puntuación del grupo Cohesión social/Calidad de vida'
        generarColormapGrupo(mapa, rankingColormapGeneral, myCaption, geojson_fields, geojson_aliases, geojson)
    elif filtros['colormapIndMedioambiente'] and not errorColormapMedi:
        myCaption = 'Puntuación del grupo Medioambiente y Movilidad'
        generarColormapGrupo(mapa, rankingColormapGeneral, myCaption, geojson_fields, geojson_aliases, geojson)
    return errorApi

def calcularRankingInd(indicator, jsonInd, indicators):
    rankingInd = []
    # Se mira si los valores altos se consideran positivos o negativos antes de ordenar los municipios
    if indicators[indicator][2]:
        for ind in jsonInd['municipalities']:
            tmp_dict = {'lugar': ind['name'], 'data': ind['years'][0][list(ind['years'][0])[-1]]}
            reverse_insort(rankingInd, tmp_dict)
    else:
        for ind in jsonInd['municipalities']:
            tmp_dict = {'lugar': ind['name'], 'data': ind['years'][0][list(ind['years'][0])[-1]]}
            insort(rankingInd, tmp_dict)
    return rankingInd
    
def actualizarRankingGeneral(rankingGeneral, rankingInd):
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

def reverse_insort(a, x):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x['data'] > a[mid]['data']:
            hi = mid
        else:
            lo = mid+1
    a.insert(lo, x)

def insort(a, x):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x['data'] < a[mid]['data']:
            hi = mid
        else:
            lo = mid+1
    a.insert(lo, x)

def generarColormapGrupo(mapa, rankingColormapGeneral, myCaption, geojson_fields, geojson_aliases, geojson):
    data = {'lugar': [], 'dato': []}
    for mun in rankingColormapGeneral:
            for munGeojson in geojson['features']:
                if munGeojson['properties']['iz_ofizial'] == mun['lugar']:
                    munGeojson['properties']['points'] = mun['points']
            data['lugar'].append(mun['lugar'])
            data['dato'].append(mun['points'])
    df = pandas.DataFrame(data)
    colormap = branca.colormap.LinearColormap(
                    colors=['red', 'orange','yellow', 'green'],
                    vmin=df.min()['dato'],
                    vmax=df.max()['dato'],
                    caption=myCaption
                ).add_to(mapa)
    st_f = lambda x: {'fillColor': colormap(int(x['properties']['points'])), 'weight': 2, 'fillOpacity': 0.5}
    geojson_fields.append('points')
    geojson_aliases.append(myCaption)
            
    folium.GeoJson(geojson,
                        style_function=st_f,
                        tooltip=folium.features.GeoJsonTooltip(fields=geojson_fields, aliases=geojson_aliases),
                        name='colormap').add_to(mapa)
    
def cargarIndicadoresSesion(idFichero):
    rutaFichero = 'templates/session_indicators/indicators' + str(idFichero) + '.json'
    indicators_raw = {}
    if os.path.exists(rutaFichero):
        with open(rutaFichero) as f:
            indicators_raw = f.read()
        return json.loads(indicators_raw)
    else:
        with open('templates/indicatorsBase.json') as f:
            indicators_raw = f.read()
        return json.loads(indicators_raw)
    
def cargarIndicadoresTodos():
    indicatorsBase = {}
    extraIndicators = {}
    with open('templates/indicatorsBase.json') as f:
        indicatorsBase_raw = f.read()
        indicatorsBase = json.loads(indicatorsBase_raw)
    with open('templates/extraIndicatorsBase.json') as f:
        extraIndicators_raw = f.read()
        extraIndicators = json.loads(extraIndicators_raw)
    indicators = {**indicatorsBase, **extraIndicators}
    return indicators
    
    
def añadirIndicadorSesion(idFichero, indId, indTipo, indName, descInd):
    rutaFichero = 'templates/session_indicators/indicators' + str(idFichero) + '.json'
    rutaFicheroExtra = 'templates/session_indicators/extraIndicators' + str(idFichero) + '.json'
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
    # Eliminar nuevo indicador de extraIndicators.json
    with open(rutaFicheroExtra, 'r') as fExtraR:
        extraIndicators_raw = fExtraR.read()
        extraIndicators = json.loads(extraIndicators_raw)
        del extraIndicators[indId]
    with open(rutaFicheroExtra, 'w') as fExtraW:
        json.dump(extraIndicators, fExtraW)

def eliminarIndicadorSesion(idFichero, indId, indTipo, indName, descInd):
    rutaFichero = 'templates/session_indicators/indicators' + str(idFichero) + '.json'
    rutaFicheroExtra = 'templates/session_indicators/extraIndicators' + str(idFichero) + '.json'
        # Si todavía no existen ficheros para esta sesión crearlos a partir de los base
    if not os.path.exists(rutaFichero):
        shutil.copyfile('templates/indicatorsBase.json', rutaFichero)
    if not os.path.exists(rutaFicheroExtra):
        shutil.copyfile('templates/extraIndicatorsBase.json', rutaFicheroExtra)
    # Eliminar indicador de indicators.json
    indicators = cargarIndicadoresSesion(idFichero)
    del indicators[indId]
    with open(rutaFichero, 'w') as fR:
        json.dump(indicators, fR)
    # Añadir indicador a extraIndicators.json
    newExtraInd = {indId: [indTipo, indName, descInd]}
    with open(rutaFicheroExtra, 'r') as fExtraR:
        extraIndicators_raw = fExtraR.read()
        extraIndicators = json.loads(extraIndicators_raw)
        extraIndicators.update(newExtraInd)
    with open(rutaFicheroExtra, 'w') as fExtraW:
        json.dump(extraIndicators, fExtraW)
    
def reiniciarIndicadoresSesion(idFichero):
    rutaFichero = 'templates/session_indicators/indicators' + str(idFichero) + '.json'
    rutaFicheroExtra = 'templates/session_indicators/extraIndicators' + str(idFichero) + '.json'
        # Si todavía no existen ficheros para esta sesión crearlos a partir de los base
    if not os.path.exists(rutaFichero):
        shutil.copyfile('templates/indicatorsBase.json', rutaFichero)
    if not os.path.exists(rutaFicheroExtra):
        shutil.copyfile('templates/extraIndicatorsBase.json', rutaFicheroExtra)
    shutil.copyfile('templates/indicatorsBase.json', rutaFichero)
    shutil.copyfile('templates/extraIndicatorsBase.json', rutaFicheroExtra)

def getAñosIndSesion(idFichero):
    añosInd = {}
    indicators = cargarIndicadoresSesion(idFichero)
    for ind in indicators:
        jsonInd = api.getIndicator(ind)
        if jsonInd != None:
            años = [list(i['years'][0].keys()) for i in jsonInd['municipalities']]
            añosInd[ind] = años[0]
        else:
            añosInd = None
            break
    return añosInd