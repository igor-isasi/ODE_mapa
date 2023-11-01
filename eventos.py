import apis
import folium

def generarEventosGenerales(mapa, filtros):
    errorApi = None
    if filtros['filtroEv2'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosConcierto()
        if jsonEventos != None:
            fg_conciertos = folium.FeatureGroup(name='conciertos')
            añadirEventos(jsonEventos, fg_conciertos)
            fg_conciertos.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv3'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosTeatro()
        if jsonEventos != None:
            fg_teatros = folium.FeatureGroup(name='teatros')
            añadirEventos(jsonEventos, fg_teatros)
            fg_teatros.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv4'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosDanza()
        if jsonEventos != None:
            fg_danzas = folium.FeatureGroup(name='danzas')
            añadirEventos(jsonEventos, fg_danzas)
            fg_danzas.add_to(mapa)
        else: 
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv5'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosConferencia()
        if jsonEventos != None:
            fg_conferencias = folium.FeatureGroup(name='conferencias')
            añadirEventos(jsonEventos, fg_conferencias)
            fg_conferencias.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv6'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosBertsolaritza()
        if jsonEventos != None:
            fg_bertsolaritza = folium.FeatureGroup(name='bertsolaritza')
            añadirEventos(jsonEventos, fg_bertsolaritza)
            fg_bertsolaritza.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv7'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosFeria()
        if jsonEventos != None:
            fg_ferias = folium.FeatureGroup(name='ferias')
            añadirEventos(jsonEventos, fg_ferias)
            fg_ferias.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv8'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosExposicion()
        if jsonEventos != None:
            fg_exposiciones = folium.FeatureGroup(name='exposiciones')
            añadirEventos(jsonEventos, fg_exposiciones)
            fg_exposiciones.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv9'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosProyeccion()
        if jsonEventos != None:
            fg_proyecciones = folium.FeatureGroup(name='proyecciones')
            añadirEventos(jsonEventos, fg_proyecciones)
            fg_proyecciones.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv10'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosFormacion()
        if jsonEventos != None:
            fg_formaciones = folium.FeatureGroup(name='formaciones')
            añadirEventos(jsonEventos, fg_formaciones)
            fg_formaciones.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv11'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosConcurso()
        if jsonEventos != None:
            fg_concursos = folium.FeatureGroup(name='concursos')
            añadirEventos(jsonEventos, fg_concursos)
            fg_concursos.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv12'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosFestival()
        if jsonEventos != None:
            fg_festivales = folium.FeatureGroup(name='festivales')
            añadirEventos(jsonEventos, fg_festivales)
            fg_festivales.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv13'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosInfantil()
        if jsonEventos != None:
            fg_infantiles = folium.FeatureGroup(name='infantiles')
            añadirEventos(jsonEventos, fg_infantiles)
            fg_infantiles.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv14'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosFiesta()
        if jsonEventos != None:
            fg_fiestas = folium.FeatureGroup(name='fiestas')
            añadirEventos(jsonEventos, fg_fiestas)
            fg_fiestas.add_to(mapa)
        else:
            errorApi = 'API de eventos culturales'
    if filtros['filtroEv15'] or filtros['filtroEv1']:
        jsonEventos = apis.getProximosOtro()
        if jsonEventos != None:
            fg_otros = folium.FeatureGroup(name='otros')
            añadirEventos(jsonEventos, fg_otros)
            fg_otros.add_to(mapa)
        else:
                errorApi = 'API de eventos culturales'
    return errorApi

def añadirEventos(jsonEventos, fg):
    myIFrame = None
    myIcon = None
    myPopup = None
    for evento in jsonEventos['items']:
        if esEuskadi(evento['provinceNoraCode']):
            if 'priceEs' in evento and tieneHoraAsignada(evento):
                myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nameEs'] + 
                                        '<br><br><strong>Tipo de evento:</strong> ' + evento['typeEs'] + 
                                        '<br><br><strong>Día de inicio:</strong> ' + evento['startDate'].split("T")[0] +
                                        '<br><br><strong>Hora de inicio:</strong> ' + evento['startDate'].split("T")[1][:-1] + 
                                        '<br><br><strong>Día de fin:</strong> ' + evento['endDate'].split("T")[0] +
                                        '<br><br><strong>Hora de fin:</strong> ' + evento['endDate'].split("T")[1][:-1] +
                                        '<br><br><strong>Precio:</strong> ' + evento['priceEs'])
            elif 'priceEs' in evento and not tieneHoraAsignada(evento):
                myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nameEs'] + 
                                        '<br><br><strong>Tipo de evento:</strong> ' + evento['typeEs'] + 
                                        '<br><br><strong>Día de inicio:</strong> ' + evento['startDate'].split("T")[0] +
                                        '<br><br><strong>Día de fin:</strong> ' + evento['endDate'].split("T")[0] +
                                        '<br><br><strong>Precio:</strong> ' + evento['priceEs'])
            elif 'priceEs' not in evento and tieneHoraAsignada(evento):
                myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nameEs'] + 
                                        '<br><br><strong>Tipo de evento:</strong> ' + evento['typeEs'] + 
                                        '<br><br><strong>Día de inicio:</strong> ' + evento['startDate'].split("T")[0] +
                                        '<br><br><strong>Hora de inicio:</strong> ' + evento['startDate'].split("T")[1][:-1] + 
                                        '<br><br><strong>Día de fin:</strong> ' + evento['endDate'].split("T")[0] +
                                        '<br><br><strong>Hora de fin:</strong> ' + evento['endDate'].split("T")[1][:-1])
            else:
                myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + evento['nameEs'] + 
                                        '<br><br><strong>Tipo de evento:</strong> ' + evento['typeEs'] + 
                                        '<br><br><strong>Día de inicio:</strong> ' + evento['startDate'].split("T")[0] +
                                        '<br><br><strong>Día de fin:</strong> ' + evento['endDate'].split("T")[0])
            myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
            myIcon = getIconoEvento(evento)
            folium.Marker(location=[evento['municipalityLatitude'], evento['municipalityLongitude']], popup = myPopup, icon = myIcon).add_to(fg)

def tieneHoraAsignada(evento):
    if (evento['startDate'].split("T")[1][:-1] == '00:00') and evento['endDate'].split("T")[1][:-1] == '00:00':
        return False
    else:
        return True

def esEuskadi(provinciaCod):
    if provinciaCod == '48' or provinciaCod == '20' or provinciaCod == '1':
        return True
    else:
        return False

def getIconoEvento(evento):
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