# core/metasploit_module.py

import subprocess
import os

def run_metasploit_exploit(rc_file_path):
    try:
        if not os.path.isfile(rc_file_path):
            return f"Erreur : le fichier {rc_file_path} est introuvable."

        cmd = ["msfconsole", "-r", rc_file_path, "-q"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Erreur Metasploit : {e}"
