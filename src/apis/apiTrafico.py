import requests

def getCamaras():
    qUrl = "https://api.euskadi.eus/traffic/v1.0/cameras/"
    qParams = {'_page': 1}
    qHeaders = {'accept': 'application/json'}
    jsonPrincipal = getJson(qUrl, qParams, qHeaders)
    if jsonPrincipal != None:
        nPaginas = jsonPrincipal['totalPages']
        myJsonList = []
        # se solicitan todas las paginas hasta conseguir todas las camaras
        for pagActual in range(1, nPaginas + 1):
            qParams = {'_page': pagActual}
            jsonActual = getJson(qUrl, qParams, qHeaders)
            if jsonActual != None:
                myJsonList.append(jsonActual)
            else:
                return None
    else:
        myJsonList = None
    return myJsonList

def getIncidenciasDia(fecha):
    año = fecha.split('-')[0]
    mes = fecha.split('-')[1]
    dia = fecha.split('-')[2]
    qUrl = "https://api.euskadi.eus/traffic/v1.0/incidences/byDate/" + str(año) + "/" + str(mes) + "/" + str(dia)
    qParams = {'_page': 1}
    qHeaders = {'accept': 'application/json'}
    jsonPrincipal = getJson(qUrl, qParams, qHeaders)
    if jsonPrincipal != None:
        nPaginas = jsonPrincipal['totalPages']
        myJsonList = []
        # se solicitan todas las paginas hasta conseguir todas las incidencias
        for pagActual in range(1, nPaginas + 1):
            qParams = {'_page': pagActual}
            jsonActual = getJson(qUrl, qParams, qHeaders)
            if jsonActual != None:
                myJsonList.append(jsonActual)
            else:
                return None
    else:
        myJsonList = None
    return myJsonList

def getJson(qUrl, qParams, qHeaders):
    try:
        response = requests.get(url=qUrl, params=qParams, headers=qHeaders, timeout=10)
        if response.ok:
            myJson = response.json()
        else:
            myJson = None
    except:
        myJson = None
    return myJson