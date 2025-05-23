# gui/sqlmap_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from core.sqlmap_module import run_sqlmap_scan

class SQLmapTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("URL cible pour SQLmap :"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.scan_button = QPushButton("Lancer le scan SQLmap")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def start_scan(self):
        url = self.url_input.text().strip()
        if not url:
            self.result_area.setPlainText("Erreur : URL vide.")
            return

        self.result_area.setPlainText("Scan SQLmap en cours...")
        result = run_sqlmap_scan(url)
        self.result_area.setPlainText(result)
