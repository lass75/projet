from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from core.nessus_module import start_nessus_scan

class NessusTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Cible pour Nessus :"))
        self.target_input = QLineEdit()
        layout.addWidget(self.target_input)

        self.scan_button = QPushButton("Lancer le scan Nessus")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def start_scan(self):
        target = self.target_input.text().strip()
        if not target:
            self.result_area.setPlainText("Erreur : cible vide.")
            return

        self.result_area.setPlainText("Scan en cours, veuillez patienter...")
        result = start_nessus_scan(target)
        self.result_area.setPlainText(result)
