import requests

def getCamaras():
    qUrl = "https://api.euskadi.eus/traffic/v1.0/cameras/"
    qParams = {'_page': 1}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
        nPaginas = myJson['totalPages']
        myJsonList = []
        # se solicitan todas las paginas hasta conseguir todas las camaras
        for pagActual in range(1, nPaginas + 1):
            qParams = {'_page': pagActual}
            response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
            if response.ok:
                myJsonList.append(response.json())
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
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    myJsonList = None
    if response.ok:
        myJson = response.json()
        nPaginas = myJson['totalPages']
        myJsonList = []
        # se solicitan todas las paginas hasta conseguir todas las incidencias
        for pagActual in range(1, nPaginas + 1):
            qParams = {'_page': pagActual}
            response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
            if response.ok:
                myJsonList.append(response.json())
            else:
                myJsonList = None
                break
    else:
        myJsonList = None
    return myJsonList