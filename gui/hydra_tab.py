# tabs/hydra_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from core.hydra_module import run_hydra_scan

class HydraTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Cible Hydra (ex: 192.168.1.1) :"))
        self.target_input = QLineEdit()
        layout.addWidget(self.target_input)

        layout.addWidget(QLabel("Nom d'utilisateur (ou chemin vers fichier -L) :"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Chemin du fichier de mots de passe :"))
        self.password_file_input = QLineEdit()
        layout.addWidget(self.password_file_input)

        layout.addWidget(QLabel("Service (ex: ssh, ftp, http-post...) :"))
        self.service_input = QLineEdit()
        self.service_input.setText("ssh")
        layout.addWidget(self.service_input)

        self.scan_button = QPushButton("Lancer Hydra")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def start_scan(self):
        target = self.target_input.text().strip()
        username = self.username_input.text().strip()
        password_file = self.password_file_input.text().strip()
        service = self.service_input.text().strip()

        if not all([target, username, password_file, service]):
            self.result_area.setPlainText("Tous les champs sont obligatoires.")
            return

        self.result_area.setPlainText("Scan Hydra en cours...")
        result = run_hydra_scan(target, username, password_file, service)
        self.result_area.setPlainText(result)
