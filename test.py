from core.nessus_module import start_nessus_scan

if __name__ == "__main__":
    cible = input("Entrez la cible Nessus à scanner (ex: 192.168.1.1): ").strip()
    if not cible:
        print("Erreur : cible vide")
    else:
        print("Lancement du scan Nessus...")
        res = start_nessus_scan(cible)
        print(res)
192