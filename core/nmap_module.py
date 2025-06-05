# core/nmap_module.py
import subprocess

def run_nmap_scan(target):
    try:
        cmd = ["nmap", "-sV", target]  # -sV pour détecter les services
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Erreur Nmap : {e}"

