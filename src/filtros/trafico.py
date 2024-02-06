from apis import apiTrafico as api
import folium
from datetime import datetime

def generarEventosTrafico(mapa, filtros, fechaIncidencia):
    myIFrame = None
    myIcon = None
    myPopup = None
    errorApi = None
    if filtros['filtroTrafCamaras']:
        listaJsonCamaras = api.getCamaras()
        if listaJsonCamaras != None:
            fg_camaras = folium.FeatureGroup(name="camaras")
            for jsonCamara in listaJsonCamaras:
                for camara in jsonCamara['cameras']:
                    if float(camara['latitude']) < 45 and float(camara['latitude']) > 42 and float(camara['longitude']) < 0:
                        myIcon = folium.Icon(color='red', icon='video-camera', prefix='fa')
                        folium.Marker(location=[camara['latitude'], camara['longitude']], icon = myIcon).add_to(fg_camaras)
            fg_camaras.add_to(mapa)
        else:
            errorApi = 'API de tráfico'
    if filtros['filtroTrafIncidencias']:
        listaJsonIncidencias = api.getIncidenciasDia(fechaIncidencia)
        if listaJsonIncidencias != None:
            fg_incidencias = folium.FeatureGroup(name="incidencias")
            for jsonInc in listaJsonIncidencias:
                for inc in jsonInc['incidences']:
                    try:
                        diaInicio = datetime.strptime(inc['startDate'].split('T')[0], "%Y-%m-%d").strftime('%d-%m-%Y')
                        if 'endDate' in inc:
                            diaFin = datetime.strptime(inc['endDate'].split('T')[0], "%Y-%m-%d").strftime('%d-%m-%Y')
                            if tieneHoraAsignada(inc):
                                myIFrame = folium.IFrame(
                                    '<font color="red">INCIDENCIA</font>' + 
                                    '<br><br><strong>Día de inicio:</strong> ' + diaInicio + 
                                    '<br><br><strong>Hora de inicio:</strong> ' + inc['startDate'].split('T')[1] + 
                                    '<br><br><strong>Día de fin:</strong> ' + diaFin + 
                                    '<br><br><strong>Hora de fin:</strong> ' + inc['endDate'].split('T')[1] + 
                                    '<br><br><strong>Tipo:</strong> ' + inc['incidenceType'] + 
                                    '<br><br><strong>Causa:</strong> ' + inc['cause'])
                            elif not tieneHoraAsignada(inc) and diaInicio != diaFin:
                                myIFrame = folium.IFrame(
                                    '<font color="red">INCIDENCIA</font>' + 
                                    '<br><br><strong>Día de inicio:</strong> ' + diaInicio + 
                                    '<br><br><strong>Día de fin:</strong> ' + diaFin + 
                                    '<br><br><strong>Tipo:</strong> ' + inc['incidenceType'] + 
                                    '<br><br><strong>Causa:</strong> ' + inc['cause'])
                            else:
                                myIFrame = folium.IFrame(
                                '<font color="red">INCIDENCIA</font>' + 
                                '<br><br><strong>Día:</strong> ' + inc['startDate'].split('T')[0] + 
                                '<br><br><strong>Tipo:</strong> ' + inc['incidenceType'] + 
                                '<br><br><strong>Causa:</strong> ' + inc['cause'])
                        elif tieneHoraInicio(inc):
                            myIFrame = folium.IFrame(
                                '<font color="red">INCIDENCIA</font>' + 
                                '<br><br><strong>Día:</strong> ' + inc['startDate'].split('T')[0] + 
                                '<br><br><strong>Hora:</strong> ' + inc['startDate'].split('T')[1] + 
                                '<br><br><strong>Tipo:</strong> ' + inc['incidenceType'] + 
                                '<br><br><strong>Causa:</strong> ' + inc['cause'])
                        else:
                            myIFrame = folium.IFrame(
                                '<font color="red">INCIDENCIA</font>' + 
                                '<br><br><strong>Día:</strong> ' + inc['startDate'].split('T')[0] + 
                                '<br><br><strong>Tipo:</strong> ' + inc['incidenceType'] + 
                                '<br><br><strong>Causa:</strong> ' + inc['cause'])
                        if float(inc['latitude']) < 45 and float(inc['latitude']) > 42 and float(inc['longitude']) < 0:
                            myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
                            myIcon = folium.Icon(color='red', icon='car', prefix='fa')
                            folium.Marker(location=[inc['latitude'], inc['longitude']],popup = myPopup, icon = myIcon).add_to(fg_incidencias)
                    except:
                        print('no se ha incluido la incidencia ' + str(inc) + ' por falta de informacion', flush=True)
            fg_incidencias.add_to(mapa)
        else:
            errorApi = 'API de tráfico'
    return errorApi

def tieneHoraAsignada(inc):
    if (inc['startDate'].split("T")[1] == '00:00') and (inc['endDate'].split('T')[1] == '00:00'):
        return False
    else:
        return True
    
def tieneHoraInicio(inc):
    if inc['startDate'].split('T')[1] == '00:00':
        return False
    else:
        return True