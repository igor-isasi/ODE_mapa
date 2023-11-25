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