import requests
import time

ZAP_API_KEY = "changeme"  # À configurer selon ton installation ZAP
ZAP_API_URL = "http://127.0.0.1:8080"

def start_zap_scan(target_url):
    try:
        # Démarre le scan actif
        scan_url = f"{ZAP_API_URL}/JSON/ascan/action/scan/?url={target_url}&apikey={ZAP_API_KEY}"
        response = requests.get(scan_url)
        scan_id = response.json().get('scan')

        # Polling pour vérifier le statut du scan
        status_url = f"{ZAP_API_URL}/JSON/ascan/view/status/?scanId={scan_id}&apikey={ZAP_API_KEY}"
        while True:
            status_resp = requests.get(status_url)
            status = status_resp.json().get('status')
            if status == '100':
                break
            time.sleep(2)

        # Récupérer les alertes trouvées
        alerts_url = f"{ZAP_API_URL}/JSON/core/view/alerts/?baseurl={target_url}&apikey={ZAP_API_KEY}"
        alerts_resp = requests.get(alerts_url)
        alerts = alerts_resp.json().get('alerts', [])

        if not alerts:
            return "Aucune vulnérabilité détectée."

        result_text = "Vulnérabilités détectées :\n"
        for alert in alerts:
            result_text += f"- {alert['alert']} (Risque : {alert['risk']})\n"

        return result_text

    except Exception as e:
        return f"Erreur OWASP ZAP : {e}"
