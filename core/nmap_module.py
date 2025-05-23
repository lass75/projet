import subprocess

def run_nmap_scan(target):
    try:
        result = subprocess.run(
            ["nmap", "-sV", target],
            capture_output=True, text=True
        )
        return result.stdout
    except Exception as e:
        return f"Erreur Nmap : {e}"
