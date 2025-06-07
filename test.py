import sys
from PyQt5.QtWidgets import QApplication
from gui.metasploit_tab import MetasploitTab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MetasploitTab()
    window.show()
    sys.exit(app.exec())

