from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import subprocess

class HydraTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Adresse IP cible :"))
        self.ip_input = QLineEdit()
        layout.addWidget(self.ip_input)

        layout.addWidget(QLabel("Port :"))
        self.port_input = QLineEdit()
        self.port_input.setText("22")  # Valeur par défaut pour SSH
        layout.addWidget(self.port_input)

        layout.addWidget(QLabel("Service (ex: ssh, ftp, http) :"))
        self.service_input = QLineEdit()
        layout.addWidget(self.service_input)

        layout.addWidget(QLabel("Fichier utilisateurs (chemin complet) :"))
        self.userlist_input = QLineEdit()
        layout.addWidget(self.userlist_input)

        layout.addWidget(QLabel("Fichier mots de passe (chemin complet) :"))
        self.passlist_input = QLineEdit()
        layout.addWidget(self.passlist_input)

        self.launch_button = QPushButton("Lancer Hydra")
        self.launch_button.clicked.connect(self.run_hydra)
        layout.addWidget(self.launch_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def run_hydra(self):
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        service = self.service_input.text().strip()
        userlist = self.userlist_input.text().strip()
        passlist = self.passlist_input.text().strip()

        if not all([ip, port, service, userlist, passlist]):
            self.result_area.setPlainText("Tous les champs sont obligatoires.")
            return

        try:
            command = [
                "hydra",
                "-L", userlist,
                "-P", passlist,
                ip,
                service,
                "-s", port
            ]
            self.result_area.setPlainText("Exécution en cours...\n")
            result = subprocess.run(command, capture_output=True, text=True)
            self.result_area.setPlainText(result.stdout + "\n" + result.stderr)
        except Exception as e:
            self.result_area.setPlainText(f"Erreur d'exécution : {e}")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Test Hydra")
    window.setCentralWidget(HydraTab())
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
