import apis
import folium
import entidades

def generarEventosAdmin(mapa, filtros, fechaEventosAdmin):
    myIFrame = None
    myIcon = None
    myPopup = None
    errorApi = None
    if filtros['filtroEvAd1']:
        listaJsonEventosAdmin = apis.getEventosAdminDia(fechaEventosAdmin)
        if listaJsonEventosAdmin != None:
            fg_eventosAdmin = folium.FeatureGroup(name="eventos administrativos")
            for jsonEvAd in listaJsonEventosAdmin:
                for evAd in jsonEvAd['events']:
                    #print(evAd, flush=True)
                    if 'entityEs' in evAd:
                        print(evAd['entityEs'], flush=True)
                        jsonEntidad = apis.getEntidad(evAd['entityEs'])
                        print(jsonEntidad, flush=True)
                        if jsonEntidad != None:
                            entidad = None
                            if jsonEntidad['totalItemsCount'] >= 1:
                                for ent in jsonEntidad['pageItems']:
                                    if evAd['entityEs'] in ent['name']:
                                        entidad = ent
                                        break
                            if entidad != None:
                                if 'geoPosition' in entidad and entidad['geoPosition']['country']['oid'] == '108' and \
                                    (entidad['geoPosition']['county']['oid'] == '01' or entidad['geoPosition']['county']['oid'] == '20' \
                                    or entidad['geoPosition']['county']['oid'] == '48'):
                                    if entidad['geoPosition']['position2D']['standard'] == 'ETRS89':
                                        lat, long = entidades.convertirCoords(entidad['geoPosition']['position2D']['x'], entidad['geoPosition']['position2D']['y'])
                                    else:
                                        lat, long = entidad['geoPosition']['position2D']['x'], entidad['geoPosition']['position2D']['y']
                                    if tieneHoraAsignada:
                                        myIFrame = folium.IFrame(
                                            '<font color="white">EVENTO ADMINISTRATIVO</font>' + 
                                            '<br><br><strong>Nombre:</strong> ' + evAd['nameEs'] +
                                            '<br><br><strong>Tipo:</strong> ' + evAd['typeEs'] +
                                            '<br><br><strong>Día de inicio:</strong> ' + evAd['startDate'].split('T')[0] + 
                                            '<br><br><strong>Hora de inicio:</strong> ' + evAd['startDate'].split('T')[1][:-1] + 
                                            '<br><br><strong>Día de fin:</strong> ' + evAd['endDate'].split('T')[0] + 
                                            '<br><br><strong>Hora de fin:</strong> ' + evAd['endDate'].split('T')[1][:-1])
                                    else:
                                        myIFrame = folium.IFrame(
                                            '<font color="white">EVENTO ADMINISTRATIVO</font>' + 
                                            '<br><br><strong>Nombre:</strong> ' + evAd['nameEs'] +
                                            '<br><br><strong>Tipo:</strong> ' + evAd['typeEs'] +
                                            '<br><br><strong>Día de inicio:</strong> ' + evAd['startDate'].split('T')[0] + 
                                            '<br><br><strong>Día de fin:</strong> ' + evAd['endDate'].split('T')[0])
                                        myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                                        myIcon = folium.Icon(color='white', icon='car', prefix='fa')
                                        folium.Marker(location=[lat, long],popup = myPopup, icon = myIcon).add_to(fg_eventosAdmin)
                                fg_eventosAdmin.add_to(mapa)
                        else:
                            errorApi = 'API de personas, entidades y equipamientos'
        else:
            errorApi = 'API de eventos administrativos'
    return errorApi

def tieneHoraAsignada(evAd):
    if evAd['startDate'].split('T')[1][:-1] == '00:00' and evAd['endDate'].split('T')[1][:-1] == '00:00':
        return False
    else:
        return True