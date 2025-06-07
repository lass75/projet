# core/hydra_module.py
import subprocess

def run_hydra_scan(target, username, password_file, service="ssh"):
    try:
        cmd = [
            "hydra",
            "-L", username,
            "-P", password_file,
            target,
            service
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Erreur Hydra : {e}"
