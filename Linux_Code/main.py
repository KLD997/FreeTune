import sys
from ui import LinOLS
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = LinOLS()
        window.show()
        exit_code = app.exec()
        window.deleteLater()
        del window
        sys.exit(exit_code)