import subprocess
import os

def start_burp():
    try:
        # Vérifie si burpsuite est installé dans le PATH
        subprocess.Popen(["burpsuite"])  # ou chemin complet ex: /opt/BurpSuiteCommunity/BurpSuiteCommunity
        return "Burp Suite a été lancé avec succès."
    except FileNotFoundError:
        return "Erreur : Burp Suite n'est pas installé ou son chemin n'est pas dans le PATH."
    except Exception as e:
        return f"Erreur lors du lancement de Burp Suite : {e}"
