import requests
import time

NESSUS_URL = "https://localhost:8834"
ACCESS_KEY = "ta_access_key"
SECRET_KEY = "ta_secret_key"

HEADERS = {
    'X-ApiKeys': f'accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}',
    'Content-Type': 'application/json'
}

def start_nessus_scan(target):
    try:
        # 1. Créer un scan simple
        scan_data = {
            "uuid": "nessus_scan_uuid_standard",  # UUID du template de scan (varie selon la version)
            "settings": {
                "name": f"Scan automatique {target}",
                "text_targets": target,
                "launch_now": True
            }
        }

        # Créer le scan
        response = requests.post(f"{NESSUS_URL}/scans", headers=HEADERS, json=scan_data, verify=False)
        response.raise_for_status()
        scan_id = response.json()['scan']['id']

        # 2. Lancer le scan
        launch_response = requests.post(f"{NESSUS_URL}/scans/{scan_id}/launch", headers=HEADERS, verify=False)
        launch_response.raise_for_status()

        # 3. Polling pour le statut
        while True:
            status_resp = requests.get(f"{NESSUS_URL}/scans/{scan_id}", headers=HEADERS, verify=False)
            status_resp.raise_for_status()
            info = status_resp.json()
            if info['info']['status'] == 'completed':
                break
            time.sleep(5)

        # 4. Récupérer les vulnérabilités détectées
        vulns = []
        for vuln in info['vulnerabilities']:
            vulns.append(f"{vuln['plugin_name']} - {vuln['severity']}")

        if not vulns:
            return "Aucune vulnérabilité détectée."

        return "Vulnérabilités détectées :\n" + "\n".join(vulns)

    except Exception as e:
        return f"Erreur Nessus : {e}"
