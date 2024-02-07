import requests

def getProximosConcierto():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 1}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosTeatro():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 2}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosDanza():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 4}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosConferencia():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 6}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosBertsolaritza():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 7}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosFeria():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 8}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosExposicion():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 9}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosProyeccion():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 3}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosFormacion():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 11}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosConcurso():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 12}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosFestival():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 13}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosInfantil():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 14}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosOtro():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 15}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getProximosFiesta():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
    qParams = {"_elements": 200, "_page": 1, "type": 16}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

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