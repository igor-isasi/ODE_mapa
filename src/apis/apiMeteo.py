import requests
import jwt
from cryptography.hazmat.primitives import serialization
import time
from datetime import date
import subprocess

def getPrediccionSemanal(zoneId, locId, fecha):
    añoActual = date.today().year
    mesActual = date.today().month
    diaActual = date.today().day
    año = fecha.split('-')[0]
    mes = fecha.split('-')[1]
    dia = fecha.split('-')[2]
    token = generarToken()
    if token != None:
        qUrl = "https://api.euskadi.eus/euskalmet/weather/regions/basque_country/zones/" + zoneId + "/locations/" + locId + "/forecast/trends/at/" + str(añoActual) + "/" + str(mesActual) + "/" + str(diaActual) + "/for/" + str(año) + str(mes) + str(dia)
        qHeaders = {'accept': 'application/json', 'Authorization' : 'Bearer ' + token}
        myJson = getJson(qUrl, qHeaders)
    else:
        myJson = None
    return myJson

def generarToken():
    try:
        ts = int(time.time())
        fingerprint = str(subprocess.getoutput('cat /run/secrets/euskalmet_fingerprint'))
        header = {
        "alg": "RS256",
        "typ": "JWT"
        }
        payload = {
        "aud": "met01.apikey",
        "iss": "UPV/EHU",
        "exp": 1734044399,
        "version": "1.0.0",
        "iat": ts,
        "loginId": fingerprint
        }
        private_key = str(subprocess.getoutput('cat /run/secrets/euskalmet_private_apikey'))
        key = serialization.load_pem_private_key(private_key.encode(), password=None)
        token = jwt.encode(headers=header, payload=payload, key=key)
        return token
    except:
        return None
    
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