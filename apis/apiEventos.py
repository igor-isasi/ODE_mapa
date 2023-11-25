import requests

def getProximosConcierto():
    qUrl = "https://api.euskadi.eus/culture/events/v1.0/events/upcoming"
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
