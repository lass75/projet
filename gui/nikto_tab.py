# gui/nikto_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from core.nikto_module import run_nikto_scan

class NiktoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("URL ou IP de la cible pour Nikto :"))
        self.target_input = QLineEdit()
        layout.addWidget(self.target_input)

        self.scan_button = QPushButton("Lancer le scan Nikto")
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

        self.result_area.setPlainText("Scan Nikto en cours...\n")
        output = run_nikto_scan(target)
        self.result_area.setPlainText(output)
