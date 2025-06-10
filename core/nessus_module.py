import requests
import time
import urllib3

# Désactiver les warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NESSUS_URL = "https://localhost:8834"
ACCESS_KEY = "acf314688239e705884eb18926d6e1f58c8d4b0fe6e728b8f2e16ff8b53015f7"
SECRET_KEY = "7d658ac3b90de078597f0ca4715c00f0881b23e3c2e832470b6570a78b358bcf"

# Headers améliorés pour éviter les connection reset
HEADERS = {
    'X-ApiKeys': f'accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}',
    'Content-Type': 'application/json',
    'Connection': 'close',  # Force fermeture après chaque requête
    'User-Agent': 'Python-Nessus/1.0'
}

def safe_request(method, url, json_data=None, max_retries=3):
    """Fonction pour requêtes robustes avec retry"""
    for attempt in range(max_retries):
        try:
            if method == 'GET':
                response = requests.get(url, headers=HEADERS, verify=False, timeout=(15, 60))
            elif method == 'POST':
                response = requests.post(url, headers=HEADERS, json=json_data, verify=False, timeout=(15, 60))
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.ConnectionError as e:
            if "Connection reset by peer" in str(e) or "Connection broken" in str(e):
                wait_time = (attempt + 1) * 2  # 2, 4, 6 secondes
                print(f"Connexion fermée par Nessus, nouvelle tentative dans {wait_time}s... ({attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                if attempt == max_retries - 1:
                    raise Exception("Impossible de maintenir la connexion avec Nessus après plusieurs tentatives")
            else:
                raise
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2)

def get_template_uuid():
    """Récupère un UUID de template valide"""
    try:
        response = safe_request('GET', f"{NESSUS_URL}/editor/scan/templates")
        templates = response.json().get('templates', [])
        
        # Chercher le template 'basic' en premier
        for template in templates:
            if template['name'] == 'basic':
                return template['uuid']
        
        # Si pas de 'basic', prendre le premier disponible
        if templates:
            print(f"Template 'basic' non trouvé, utilisation de '{templates[0]['name']}'")
            return templates[0]['uuid']
        
        raise Exception("Aucun template disponible")
        
    except Exception as e:
        # UUID par défaut pour versions courantes de Nessus
        print(f"Impossible de récupérer les templates ({e}), utilisation UUID par défaut")
        return "731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6"  # UUID basic scan courant

def start_nessus_scan(target):
    try:
        print(f"Démarrage du scan pour {target}")
        
        # 1. Récupérer un UUID de template valide
        template_uuid = get_template_uuid()
        
        # 2. Créer un scan
        scan_data = {
            "uuid": template_uuid,
            "settings": {
                "name": f"Scan automatique {target}",
                "text_targets": target,
                "launch_now": False  # Créer d'abord, lancer ensuite
            }
        }
        
        print("Création du scan...")
        response = safe_request('POST', f"{NESSUS_URL}/scans", scan_data)
        scan_id = response.json()['scan']['id']
        print(f"Scan créé avec ID: {scan_id}")
        
        # 3. Lancer le scan
        print("Lancement du scan...")
        safe_request('POST', f"{NESSUS_URL}/scans/{scan_id}/launch")
        print("Scan lancé, surveillance en cours...")
        
        # 4. Polling pour le statut avec gestion des erreurs de connexion
        start_time = time.time()
        last_status = None
        
        while True:
            try:
                status_resp = safe_request('GET', f"{NESSUS_URL}/scans/{scan_id}")
                info = status_resp.json()
                
                current_status = info['info']['status']
                progress = info['info'].get('progress', 0)
                
                # Afficher le progrès seulement s'il change
                if current_status != last_status:
                    elapsed = int(time.time() - start_time)
                    print(f"[{elapsed//60:02d}:{elapsed%60:02d}] Statut: {current_status} - {progress}%")
                    last_status = current_status
                
                if current_status == 'completed':
                    print("Scan terminé!")
                    break
                elif current_status in ['aborted', 'canceled', 'stopped']:
                    return f"Scan interrompu: {current_status}"
                elif current_status == 'empty':
                    return "Aucune cible accessible pour le scan"
                
                # Attendre avant la prochaine vérification
                time.sleep(10)  # Vérification toutes les 10 secondes
                
            except Exception as e:
                print(f"Erreur lors de la surveillance: {e}")
                time.sleep(5)
                # Continuer la surveillance même en cas d'erreur ponctuelle
        
        # 5. Récupérer les vulnérabilités détectées
        print("Récupération des résultats...")
        final_resp = safe_request('GET', f"{NESSUS_URL}/scans/{scan_id}")
        final_info = final_resp.json()
        
        # Formater les résultats
        vulnerabilities = final_info.get('vulnerabilities', [])
        if not vulnerabilities:
            return "✅ Aucune vulnérabilité détectée."
        
        # Trier par gravité (plus graves d'abord)
        severity_order = {4: 'Critique', 3: 'Élevée', 2: 'Moyenne', 1: 'Faible', 0: 'Info'}
        vulns_sorted = sorted(vulnerabilities, key=lambda x: x.get('severity', 0), reverse=True)
        
        # Construire la liste des vulnérabilités
        vulns = []
        for vuln in vulns_sorted[:20]:  # Limiter à 20 pour éviter des réponses trop longues
            severity_num = vuln.get('severity', 0)
            severity_text = severity_order.get(severity_num, 'Inconnue')
            plugin_name = vuln.get('plugin_name', 'Vulnérabilité inconnue')
            count = vuln.get('count', 1)
            
            vuln_line = f"[{severity_text}] {plugin_name}"
            if count > 1:
                vuln_line += f" ({count}x)"
            vulns.append(vuln_line)
        
        result = f"🔍 Vulnérabilités détectées ({len(vulnerabilities)} total):\n\n"
        result += "\n".join(vulns)
        
        if len(vulnerabilities) > 20:
            result += f"\n\n... et {len(vulnerabilities) - 20} autres vulnérabilités"
        
        return result
        
    except requests.exceptions.ConnectionError as e:
        if "Connection reset by peer" in str(e):
            return "❌ Erreur: Nessus ferme les connexions de manière inattendue. Vérifiez la configuration du serveur Nessus ou essayez de redémarrer le service."
        else:
            return f"❌ Erreur de connexion: {e}"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return "❌ Erreur d'authentification: Vérifiez vos clés ACCESS_KEY et SECRET_KEY"
        elif e.response.status_code == 403:
            return "❌ Accès refusé: Permissions insuffisantes"
        else:
            return f"❌ Erreur HTTP {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Erreur Nessus: {e}"

# Test de connexion
def test_nessus_connection():
    """Teste la connexion à Nessus"""
    try:
        response = safe_request('GET', f"{NESSUS_URL}/server/status")
        data = response.json()
        status = data.get('status', 'unknown')
        version = data.get('version', 'N/A')
        return f"✅ Connexion réussie - Statut: {status}, Version: {version}"
    except Exception as e:
        return f"❌ Test de connexion échoué: {e}"

# Pour tester
if __name__ == "__main__":
    print("=== TEST DE CONNEXION NESSUS ===")
    print(test_nessus_connection())
    

    print("\n=== TEST DE SCAN ===")
    result = start_nessus_scan("127.0.0.1")
    print(result)