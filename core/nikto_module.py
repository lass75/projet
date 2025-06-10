import subprocess

def run_nikto_scan(target):
    try:
        result = subprocess.run(
            ["nikto", "-h", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.stderr:
            return f"Erreur Nikto : {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Erreur Nikto : {e}"
