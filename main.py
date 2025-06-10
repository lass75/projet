from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
import sys

# Importe tes tabs (onglets) que tu as déjà codés
from gui.nmap_tab import NmapTab
from gui.sqlmap_tab import SQLmapTab
from gui.zap_tab import ZapTab
from gui.metasploit_tab import MetasploitTab
from gui.hydra_tab import HydraTab
from gui.burp_tab import BurpTab
from gui.nessus_tab import NessusTab
from gui.john_tab import JohnTab
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
        self.tabs.addTab(HydraTab(), "Hydra")
        self.tabs.addTab(ZapTab(), "OWASP ZAP")
        self.tabs.addTab(MetasploitTab(), "Metasploit")
        self.tabs.addTab(BurpTab(),"Burpsuite")
        self.tabs.addTab(NessusTab(),"Nessus")
        self.tabs.addTab(JohnTab(),"John The Ripper")
        # Ajouter les autres onglets ici

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())