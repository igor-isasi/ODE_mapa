import requests

def getCentrosSanitarios():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'HEALTH'}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getEntidadesReligiosas():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'RELIGIOUS'}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getEntidadesLegislativas():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'LEGISLATIVE'}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getEntidadesJudiciales():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'JUDICIAL'}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getEntidadesPartidos():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'POLITICAL_PARTY'}
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qParams, qHeaders)

def getFundaciones():
    qUrl = "https://api.euskadi.eus/directory/entities"
    qParams = {'pageSize': 100, 'subType': 'FOUNDATION'}
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