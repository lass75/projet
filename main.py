from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
import sys

# Importe tes tabs (onglets) que tu as déjà codés
from gui.nmap_tab import NmapTab
from gui.sqlmap_tab import SQLmapTab
from gui.zap_tab import ZapTab
# à compléter avec les autres outils

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toolbox de Scan Sécurité")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Ajouter les onglets
        self.tabs.addTab(NmapTab(), "Nmap")
        self.tabs.addTab(SQLmapTab(), "SQLMap")
        self.tabs.addTab(ZapTab(), "OWASP ZAP")
        # Ajouter les autres onglets ici

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())