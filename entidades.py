import apis
import folium
from pyproj import Transformer

def generarEntidades(mapa, filtros):
    errorApi = None
    if filtros['filtroEn2'] or filtros['filtroEn1']:
        jsonEntidades = apis.getCentrosDeSalud()
        if jsonEntidades != None:
            fg_centrosDeSalud = folium.FeatureGroup(name='centros de salud')
            añadirEntidades(jsonEntidades['pageItems'], fg_centrosDeSalud)
            fg_centrosDeSalud.add_to(mapa)
        else:
            errorApi = 'API de personas, entidades y equipamientos'
    return errorApi
    
def añadirEntidades(jsonEntidades, fg):
    myIFrame = None
    myIcon = None
    myPopup = None
    for entidad in jsonEntidades:
        myIFrame = folium.IFrame('<strong>Nombre:</strong> ' + entidad['name'] + 
                                        '<br><br><strong>Tipo de entidad:</strong> ' + entidad['subType']['name'])
        myPopup = folium.Popup(myIFrame, min_width=300, max_width=500)
        #myIcon = getIconoEntidad(entidad)
        lat, long = convertirCoords(entidad['geoPosition']['position2D']['x'], entidad['geoPosition']['position2D']['y'])
        folium.Marker(location=[lat, long], popup = myPopup, icon = myIcon).add_to(fg)

def convertirCoords(utm_x, utm_y):
    huso = 30
    transformer = Transformer.from_crs({'proj': "utm", 'zone': huso}, {'proj': 'longlat'})
    long,lat = transformer.transform(utm_x, utm_y)
    return lat,long