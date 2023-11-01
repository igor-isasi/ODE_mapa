import apis
import folium
from pyproj import Transformer

def generarEntidades(mapa, filtros):
    errorApi = None
    if filtros['filtroEn2'] or filtros['filtroEn1']:
        jsonEntidades = apis.getCentrosSanitarios()
        if jsonEntidades != None:
            fg_centrosSanitarios = folium.FeatureGroup(name='centros sanitarios')
            añadirEntidades(jsonEntidades['pageItems'], fg_centrosSanitarios)
            fg_centrosSanitarios.add_to(mapa)
        else:
            errorApi = 'API de personas, entidades y equipamientos'
    if filtros['filtroEn3'] or filtros['filtroEn1']:
        jsonEntidades = apis.getEntidadesReligiosas()
        if jsonEntidades != None:
            fg_entidadesReligiosas = folium.FeatureGroup(name='entidades religiosas')
            añadirEntidades(jsonEntidades['pageItems'], fg_entidadesReligiosas)
            fg_entidadesReligiosas.add_to(mapa)
        else:
            errorApi = 'API de personas, entidades y equipamientos'
    if filtros['filtroEn4'] or filtros['filtroEn1']:
        jsonEntidades = apis.getEntidadesLegislativas()
        if jsonEntidades != None:
            fg_entidadesLegislativas = folium.FeatureGroup(name='entidades legislativas')
            añadirEntidades(jsonEntidades['pageItems'], fg_entidadesLegislativas)
            fg_entidadesLegislativas.add_to(mapa)
        else:
            errorApi = 'API de personas, entidades y equipamientos'
    if filtros['filtroEn5'] or filtros['filtroEn1']:
        jsonEntidades = apis.getEntidadesJudiciales()
        if jsonEntidades != None:
            fg_entidadesJudiciales = folium.FeatureGroup(name='entidades judiciales')
            añadirEntidades(jsonEntidades['pageItems'], fg_entidadesJudiciales)
            fg_entidadesJudiciales.add_to(mapa)
        else:
            errorApi = 'API de personas, entidades y equipamientos'
    if filtros['filtroEn6'] or filtros['filtroEn1']:
        jsonEntidades = apis.getEntidadesPartidos()
        if jsonEntidades != None:
            fg_entidadesPartidos = folium.FeatureGroup(name='entidades de partidos políticos')
            añadirEntidades(jsonEntidades['pageItems'], fg_entidadesPartidos)
            fg_entidadesPartidos.add_to(mapa)
        else:
            errorApi = 'API de personas, entidades y equipamientos'
    if filtros['filtroEn7'] or filtros['filtroEn1']:
        jsonEntidades = apis.getFundaciones()
        if jsonEntidades != None:
            fg_fundaciones = folium.FeatureGroup(name='fundaciones')
            añadirEntidades(jsonEntidades['pageItems'], fg_fundaciones)
            fg_fundaciones.add_to(mapa)
        else:
            errorApi = 'API de personas, entidades y equipamientos'
    return errorApi
    
def añadirEntidades(jsonEntidades, fg):
    myIFrame = None
    myIcon = None
    myPopup = None
    for entidad in jsonEntidades:
        if 'geoPosition' in entidad and entidad['geoPosition']['country']['oid'] == '108' and \
            (entidad['geoPosition']['county']['oid'] == '01' or entidad['geoPosition']['county']['oid'] == '20' \
              or entidad['geoPosition']['county']['oid'] == '48'):
            myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + entidad['name'] + 
                                            '<br><br><strong>Tipo de entidad:</strong> ' + entidad['subType']['name'])
            myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
            myIcon = getIconoEntidad(entidad)
            if entidad['geoPosition']['position2D']['standard'] == 'ETRS89':
                lat, long = convertirCoords(entidad['geoPosition']['position2D']['x'], entidad['geoPosition']['position2D']['y'])
            else:
                lat, long = entidad['geoPosition']['position2D']['x'], entidad['geoPosition']['position2D']['y']
            folium.Marker(location=[lat, long], popup = myPopup, icon = myIcon).add_to(fg)
        else:
            print(entidad, flush=True)

def getIconoEntidad(entidad):
    myIcon = folium.Icon(color='gray', icon='question', prefix='fa')
    if entidad['subType']['id'] == 'HEALTH': #centros sanitarios
        myIcon = folium.Icon(color='gray', icon='house-medical', prefix='fa')
    if entidad['subType']['id'] == 'RELIGIOUS': #entidades religiosas
        myIcon = folium.Icon(color='gray', icon='cross', prefix='fa')
    if entidad['subType']['id'] == 'LEGISLATIVE': #entidades legislativas
        myIcon = folium.Icon(color='gray', icon='scale-balanced', prefix='fa')
    if entidad['subType']['id'] == 'JUDICIAL': #entidades judiciales
        myIcon = folium.Icon(color='gray', icon='gavel', prefix='fa')
    if entidad['subType']['id'] == 'POLITICAL_PARTY': #entidades de partidos politicos
        myIcon = folium.Icon(color='gray', icon='flag', prefix='fa')
    if entidad['subType']['id'] == 'FOUNDATION': #fundaciones
        myIcon = folium.Icon(color='gray', icon='people-group', prefix='fa')
    return myIcon

def convertirCoords(utm_x, utm_y):
    huso = 30
    transformer = Transformer.from_crs({'proj': "utm", 'zone': huso}, {'proj': 'longlat'})
    long,lat = transformer.transform(utm_x, utm_y)
    return lat,long