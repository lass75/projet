# core/sqlmap_module.py
import subprocess

def run_sqlmap_scan(url):
    try:
        cmd = ["python", "C:\\sqlmap\\sqlmap.py", "-u", url, "--batch", "--level=2"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Erreur SQLmap : {e}"
