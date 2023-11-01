import apis
import folium

def generarEventosTrafico(mapa, filtros, fechaIncidencia):
    myIFrame = None
    myIcon = None
    myPopup = None
    errorApi = None
    if filtros['filtroTraf1']:
        listaJsonCamaras = apis.getCamaras()
        if listaJsonCamaras != None:
            fg_camaras = folium.FeatureGroup(name="camaras")
            for jsonCamara in listaJsonCamaras:
                for camara in jsonCamara['cameras']:
                    if float(camara['latitude']) < 45 and float(camara['longitude']) < 0:
                        myIcon = folium.Icon(color='red', icon='video-camera', prefix='fa')
                        folium.Marker(location=[camara['latitude'], camara['longitude']], icon = myIcon).add_to(fg_camaras)
            fg_camaras.add_to(mapa)
        else:
            errorApi = 'API de tráfico'
    if filtros['filtroTraf2']:
        listaJsonIncidencias = apis.getIncidenciasDia(fechaIncidencia)
        if listaJsonIncidencias != None:
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
        else:
            errorApi = 'API de tráfico'
    return errorApi