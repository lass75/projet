from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
from core.john_module import run_john, show_cracked_passwords

class JohnTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Chemin du fichier de hash :"))
        self.hash_input = QLineEdit()
        layout.addWidget(self.hash_input)

        browse_hash = QPushButton("Parcourir...")
        browse_hash.clicked.connect(self.browse_hash_file)
        layout.addWidget(browse_hash)

        layout.addWidget(QLabel("Chemin du fichier wordlist (optionnel) :"))
        self.wordlist_input = QLineEdit()
        layout.addWidget(self.wordlist_input)

        browse_wordlist = QPushButton("Parcourir...")
        browse_wordlist.clicked.connect(self.browse_wordlist_file)
        layout.addWidget(browse_wordlist)

        self.scan_button = QPushButton("Lancer John")
        self.scan_button.clicked.connect(self.run_john_scan)
        layout.addWidget(self.scan_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def browse_hash_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier de hash")
        if file_path:
            self.hash_input.setText(file_path)

    def browse_wordlist_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier wordlist")
        if file_path:
            self.wordlist_input.setText(file_path)

    def run_john_scan(self):
        hash_file = self.hash_input.text().strip()
        wordlist = self.wordlist_input.text().strip() or None

        if not hash_file:
            self.result_area.setPlainText("Erreur : chemin du fichier hash manquant.")
            return

        self.result_area.setPlainText("Crackage en cours avec John...\n")
        output = run_john(hash_file, wordlist)
        self.result_area.append(output)

        self.result_area.append("\nMots de passe trouvés :\n")
        cracked = show_cracked_passwords()
        self.result_area.append(cracked)
