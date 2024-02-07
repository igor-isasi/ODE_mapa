import requests

def getIndicator(indicator):
    qUrl = "https://api.euskadi.eus/udalmap/indicators/" + str(indicator) + "/municipalities"
    qHeaders = {'accept': 'application/json'}
    return getJson(qUrl, qHeaders)

def getJson(qUrl, qHeaders):
    try:
        response = requests.get(url=qUrl, headers=qHeaders, timeout=10)
        if response.ok:
            myJson = response.json()
        else:
            myJson = None
    except:
        myJson = None
    return myJson