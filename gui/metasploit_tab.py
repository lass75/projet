# gui/metasploit_tab.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from core.metasploit_module import run_metasploit_exploit

class MetasploitTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Chemin vers le fichier .rc de Metasploit :"))
        self.rc_input = QLineEdit()
        layout.addWidget(self.rc_input)

        self.scan_button = QPushButton("Lancer Metasploit")
        self.scan_button.clicked.connect(self.start_msf)
        layout.addWidget(self.scan_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def start_msf(self):
        rc_path = self.rc_input.text().strip()
        if not rc_path:
            self.result_area.setPlainText("Erreur : chemin du fichier .rc vide.")
            return

        self.result_area.setPlainText("Exécution Metasploit...")
        result = run_metasploit_exploit(rc_path)
        self.result_area.setPlainText(result)
