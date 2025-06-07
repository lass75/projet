from core.nmap_module import run_nmap_scan

if __name__ == "__main__":
    target = input("Entrez l'IP ou domaine à scanner avec Nmap : ").strip()
    if not target:
        print("Erreur : cible vide.")
    else:
        print("Lancement du scan...")
        result = run_nmap_scan(target)
        print(result)
