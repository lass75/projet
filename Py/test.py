from core.zap_module import start_zap_scan

if __name__ == "__main__":
    target_url = input("Entrez l'URL cible à scanner avec OWASP ZAP : ").strip()
    if not target_url:
        print("Erreur : URL vide.")
    else:
        print("Lancement du scan...")
        result = start_zap_scan(target_url)
        print("Résultat du scan :\n")
        print(result)
