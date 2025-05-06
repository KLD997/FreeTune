from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QApplication
from PyQt6.QtCore import Qt

class ValueDialog(QDialog):
    def __init__(self, ui=None):
        super().__init__()
        self.ui = ui
        self.selected_value = ""
        self.selected_button = None  # Variable to keep track of the selected button
        self.setup_ui()

    def setup_ui(self):
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
                    min-width: 30px;
                }
                QPushButton:hover {
                    background-color: #666;
                    color: #fff;
                }
                QPushButton:pressed{
                    background-color: #444;
                    color: white;
                }
                """

        self.setWindowTitle("Value Changer")
        self.setFixedSize(250, 150)
        self.setStyleSheet("background-color: #333;")

        self.setWindowIcon(self.ui.logo_icon)

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)

        main_layout = QVBoxLayout(self)

        self.entry = QLineEdit(self)
        self.entry.setStyleSheet("""
            border: 2px;
            border-radius: 5px;
            font-family: 'Roboto';
            font-size: 14px;
            font-weight: 650;
            background-color: #555;
            height: 25px;
            width: 28px;
        """)
        self.entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entry.setFocus()
        main_layout.addWidget(self.entry)

        button_layout = QHBoxLayout()

        buttons = [
            ("=", self.change_value),
            ("+", self.change_value),
            ("-", self.change_value),
            ("%", self.change_value)
        ]
        for text, func in buttons:
            button = QPushButton(text, self)
            button.setStyleSheet(button_style)
            button.clicked.connect(lambda checked, val=text, btn=button: func(val, btn))
            button_layout.addWidget(button)

        main_layout.addLayout(button_layout)

        ok_button = QPushButton("Ok", self)
        ok_button.setStyleSheet(button_style)
        ok_button.clicked.connect(self.calculate)
        main_layout.addWidget(ok_button)

    def change_value(self, value, button):
        self.selected_value = value
        if self.selected_button is not None:
            self.selected_button.setEnabled(True)
        self.selected_button = button
        self.selected_button.setEnabled(False)
    def calculate(self):
        if not self.selected_value:
            entry_message = ""
            if self.entry.text() == "":
                entry_message += "and enter a value in the entry box"
            self.show_error(f"Please select an operation {entry_message}!")
            return

        if self.entry.text() == "":
            self.show_error("Please enter a value in the entry box!")
            return

        try:
            value = float(self.entry.text())
            if value < 0 or value > 65535:
                raise ValueError
        except ValueError:
            self.show_error("Please enter a valid number")
            return

        if not self.ui.file_path: # change
            self.show_error("No file is currently open. Please open a file first.")
            self.close()
            return

        if self.selected_value == "=":
            self.ui.text_addons.set_text(value)
        elif self.selected_value == "+":
            self.ui.text_addons.increase_selected_text(value)
        elif self.selected_value == "-":
            self.ui.text_addons.increase_selected_text(value * -1)
        elif self.selected_value == "%":
            self.ui.text_addons.increase_selected_text_per(value)

        self.ui.dialog_terminate = False
        self.close()

    def show_error(self, message):
        QMessageBox.warning(self, "Warning", message)