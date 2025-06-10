import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NESSUS_URL = "https://localhost:8834"
ACCESS_KEY = "584026324814e1d26012008dd59b04842d681e47c1d7764d8827b101c05f362c"
SECRET_KEY = "f342d70b60c7dddf8c58dfbea2f0bde22328c579c7a0c707a8306d30e53c8c39"

HEADERS = {
    "X-ApiKeys": f"accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(f"{NESSUS_URL}/server/status", headers=HEADERS, verify=False)
    print(f"Status code: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Erreur : {e}")
