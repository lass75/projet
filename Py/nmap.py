from core.nmap_module import run_nmap_scan

# Exemple d'IP locale ou cible à scanner
target = "127.0.0.1"  # ou "scanme.nmap.org" pour tester en ligne

result = run_nmap_scan(target)
print(result)
