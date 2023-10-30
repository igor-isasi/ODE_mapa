import requests

def getIndicator(indicator):
    qUrl = "https://api.euskadi.eus/udalmap/indicators/" + str(indicator) + "/municipalities"
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

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
            myJsonList.append(response.json())
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
            myJsonList.append(response.json())
    else:
        myJsonList = None
    return myJsonList

def getProximosConcierto():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming3"
    qParams = {"_elements": 200, "_page": 1, "type": 1}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosTeatro():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 2}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosDanza():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 4}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosConferencia():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 6}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosBertsolaritza():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 7}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosFeria():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 8}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosExposicion():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 9}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosProyeccion():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 3}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosFormacion():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 11}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosConcurso():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 12}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosFestival():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 13}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosInfantil():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 14}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosOtro():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 15}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getProximosFiesta():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 16}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getCentrosDeSalud():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'HEALTH'}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson