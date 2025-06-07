import subprocess

def run_john(hash_file, wordlist_path=None):
    try:
        # Commande de base
        cmd = ["john", hash_file]
        
        # Ajout du wordlist si spécifié
        if wordlist_path:
            cmd += ["--wordlist=" + wordlist_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    except Exception as e:
        return f"Erreur John the Ripper : {e}"


def show_cracked_passwords():
    try:
        result = subprocess.run(["john", "--show", "hashes.txt"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Erreur récupération des mots de passe : {e}"
