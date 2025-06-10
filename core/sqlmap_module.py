# core/sqlmap_module.py
import subprocess

def run_sqlmap_scan(url):
    try:
        cmd = ["sqlmap", "-u", url, "--batch", "--level=2"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return result.stdout
    

    except subprocess.TimeoutExpired:
        return "Erreur SQLmap: le scan a expiré"
    except Exception as e:
        return f"Erreur SQLmap : {e}"
