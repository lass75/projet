from flask import Flask, render_template, request, redirect, url_for, session
from core.nmap_module import run_nmap_scan
from core.sqlmap_module import run_sqlmap_scan
from core.zap_module import start_zap_scan
from core.hydra_module import run_hydra_scan
from core.metasploit_module import run_metasploit_exploit
from core.nikto_module import run_nikto_scan
from core.john_module import run_john
from core.nessus_module import start_nessus_scan
app = Flask(__name__)
app.secret_key = "ta_cle_secrete_ici"  # CHANGE CETTE CLE POUR LA PROD !

# Simple utilisateur admin/admin
USERNAME = "admin"
PASSWORD = "admin"

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user == USERNAME and pwd == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            error = "Identifiant ou mot de passe incorrect."
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

def handle_tool(template, form_data, func, params):
    result = None
    if request.method == "POST":
        args = [request.form.get(param) for param in params]
        result = func(*args)
    return render_template(template, result=result)

@app.route("/nmap", methods=["GET","POST"])
@login_required
def nmap():
    return handle_tool("nmap.html", request.form, run_nmap_scan, ["target"])

@app.route("/sqlmap", methods=["GET","POST"])
@login_required
def sqlmap():
    return handle_tool("sqlmap.html", request.form, run_sqlmap_scan, ["url"])

@app.route("/zap", methods=["GET","POST"])
@login_required
def zap():
    return handle_tool("zap.html", request.form, start_zap_scan, ["url"])

@app.route("/hydra", methods=["GET","POST"])
@login_required
def hydra():
    return handle_tool("hydra.html", request.form, run_hydra_scan, ["target","username","password_file","service"])

@app.route("/metasploit", methods=["GET","POST"])
@login_required
def metasploit():
    return handle_tool("metasploit.html", request.form, run_metasploit_exploit, ["rc_path"])

@app.route("/nikto", methods=["GET","POST"])
@login_required
def nikto():
    return handle_tool("nikto.html", request.form, run_nikto_scan, ["target"])


@app.route("/john", methods=["GET", "POST"])
@login_required
def john():
    return handle_tool("john.html", request.form, run_john, ["hash_file"])

@app.route("/nessus", methods=["GET", "POST"])
@login_required
def nessus():
    return handle_tool("nessus.html", request.form, start_nessus_scan, ["target"])

if __name__ == "__main__":
    app.run(debug=True)
