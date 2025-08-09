from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt

class HexAddressDialog(QDialog):
    def __init__(self, ui):
        super().__init__(ui)
        self.ui = ui

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Find Hex Address")
        self.setFixedSize(200, 120)
        self.setStyleSheet("background-color: #333;")

        self.setWindowIcon(self.ui.logo_icon)

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)

        button_style = """
            QPushButton {
                background-color: #444;
                color: white;
                font-family: 'Roboto', sans-serif;
                font-size: 12px;
                font-weight: 650;
                padding: 6px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #666;
                color: #fff;
            }
            QPushButton:pressed{
                background-color: #444;
                color: white;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #aaa;
            }
        """

        layout = QVBoxLayout()

        label = QLabel("Enter a hex address:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            border: 0;
            color: white;
            font-family: 'Roboto';
            font-size: 16px;
            font-weight: 650;
            background: transparent;
        """)
        layout.addWidget(label)

        self.find_entry = QLineEdit()
        self.find_entry.setStyleSheet("""
            border: 2px;
            border-radius: 5px;
            font-family: 'Roboto';
            font-size: 14px;
            font-weight: 650;
            background-color: #555;
            height: 25px;
            width: 28px;
            color: white;                 
        """)
        layout.addWidget(self.find_entry)

        button_find = QPushButton("Find")
        button_find.setStyleSheet(button_style)
        button_find.clicked.connect(self.find_hex)
        layout.addWidget(button_find)

        self.setLayout(layout)

    def find_hex(self):
        try:
            index = int(self.find_entry.text(), 16)
            if index % 2 != 0:
                raise ValueError
            index = index // 2
            if index < 0 or index > len(self.ui.unpacked):
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid hex address!")
            self.find_entry.setFocus()
            return

        self.highlight_hex(index)
        self.accept()

    def highlight_hex(self, index):
        selection_model = self.ui.table_view.selectionModel()
        selection_model.clearSelection()

        self.ui.mode2d.highlight_text(index, True)
        self.ui.mode2d.text_to_2d(self.ui)
