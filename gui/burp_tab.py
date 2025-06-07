from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from core.burp_module import start_burp

class BurpTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Lancement de Burp Suite :"))

        self.launch_button = QPushButton("Lancer Burp Suite")
        self.launch_button.clicked.connect(self.run_burp)
        layout.addWidget(self.launch_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        layout.addWidget(QLabel(
            "⚠️ N'oubliez pas de configurer votre navigateur pour qu'il utilise le proxy local :\n"
            "Adresse : 127.0.0.1  |  Port : 8080"
        ))

        self.setLayout(layout)

    def run_burp(self):
        result = start_burp()
        self.result_area.setPlainText(result)
