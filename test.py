from core.nikto_module import run_nikto_scan

if __name__ == "__main__":
    target = input("Entrez la cible à scanner avec Nikto (ex: http://127.0.0.1) : ").strip()
    if not target:
        print("Erreur : cible vide.")
    else:
        print("Lancement du scan Nikto...")
        result = run_nikto_scan(target)
        print("\nRésultat du scan :\n")
        print(result)