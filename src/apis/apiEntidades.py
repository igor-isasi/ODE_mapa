import requests

def getCentrosSanitarios():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'HEALTH'}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getEntidadesReligiosas():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'RELIGIOUS'}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getEntidadesLegislativas():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'LEGISLATIVE'}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getEntidadesJudiciales():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'JUDICIAL'}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getEntidadesPartidos():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'POLITICAL_PARTY'}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson

def getFundaciones():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'FOUNDATION'}
    qHeaders = {'accept': 'application/json'}
    response = requests.get(url=qUrl, params=qParams, headers=qHeaders)
    if response.ok:
        myJson = response.json()
    else:
        myJson = None
    return myJson