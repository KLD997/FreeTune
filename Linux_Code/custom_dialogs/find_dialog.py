from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QMessageBox
from PyQt6.QtCore import Qt

class CustomLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_V and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.parent().edit_pasted_values()
        else:
            super().keyPressEvent(event)

class FindDialog(QDialog):
    def __init__(self, ui):
        super().__init__(ui)
        self.ui = ui

        self.setWindowTitle("Find")
        self.setFixedSize(200, 120)
        self.setStyleSheet("background-color: #333; color: white;")

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)

        self.ui.dialog_terminate = False

        self.init_ui()

    def init_ui(self):
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
                min-width: 45px;
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

        label = QLabel("Enter the value:")
        label.setStyleSheet("""
            border: 0;
            color: white;
            font-family: 'Roboto';
            font-size: 18px;
            font-weight: 650;
            background: transparent;
        """)

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.find_entry = CustomLineEdit(self)
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

        self.find_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shortcut = QShortcut(QKeySequence("Return"), self.find_entry)
        shortcut.activated.connect(self.find_value)

        btn_find = QPushButton("Find")
        btn_find.setStyleSheet(button_style)
        btn_find.clicked.connect(self.find_value)

        btn_prev = QPushButton("Previous")
        btn_prev.setStyleSheet(button_style)
        btn_prev.clicked.connect(lambda: self.find_move(True))

        btn_next = QPushButton("Next")
        btn_next.setStyleSheet(button_style)
        btn_next.clicked.connect(lambda: self.find_move(False))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.find_entry)

        h_layout = QHBoxLayout()
        h_layout.addWidget(btn_prev)
        h_layout.addWidget(btn_next)
        h_layout.addWidget(btn_find)

        layout.setContentsMargins(5, 0, 5, 5)  # left, top, right, bottom

        layout.addLayout(h_layout)
        self.setLayout(layout)

    def find_value(self):
        value_found = False
        found_value_index = 0
        text = self.find_entry.text()
        if ',' in text:
            try:
                values = text.split(',')

                int_values = []
                for item in values:
                    value = int(item)
                    if value < 0 or value > 65535:
                        raise ValueError
                    int_values.append(value)

                int_values = tuple(int_values)

            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Please enter valid numbers!")
                return

            for i in range(len(self.ui.current_values)):
                if tuple(self.ui.current_values[i:i + len(int_values)]) == int_values:
                    found_value_index = i
                    value_found = True
                    break
        else:
            try:
                value = int(text)
                if value < 0 or value > 65535:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Please enter a valid number!")
                return

            for i in range(len(self.ui.current_values)):
                if self.ui.current_values[i] == value:
                    found_value_index = i
                    value_found = True
                    break

        if not value_found:
            QMessageBox.warning(self.ui, "Warning", "No matching value was found.")
            return

        selection_model = self.ui.table_view.selectionModel()
        selection_model.clearSelection()

        self.ui.mode2d.highlight_text(found_value_index - self.ui.shift_count, True)
        self.ui.mode2d.text_to_2d(self.ui)

    def find_move(self, previous):
        text = self.find_entry.text()
        if ',' in text:
            try:
                values = text.split(',')

                int_values = []
                for item in values:
                    value = int(item)
                    if value < 0 or value > 65535:
                        raise ValueError
                    int_values.append(value)

                int_values = tuple(int_values)

            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Please enter valid numbers!")
                return
        else:
            try:
                value = int(text)
                if value < 0 or value > 65535:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Please enter a valid number!")
                return

        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if not selected_indexes:
            visible_rect = self.ui.table_view.viewport().geometry()
            first_visible_row = self.ui.table_view.indexAt(visible_rect.topLeft()).row()

            index = first_visible_row * self.ui.columns
        else:
            selected_index = selected_indexes[0]
            row = selected_index.row()
            col = selected_index.column()

            index = (row * self.ui.columns) + col

        value_found = False

        found_value_index = 0

        if previous:
            if ',' in text:
                for i in range(index - 1, -1, -1):
                    if tuple(self.ui.current_values[i:i + len(int_values)]) == int_values:
                        found_value_index = i
                        value_found = True
                        break
            else:
                for i in range(index - 1, -1, -1):
                    if self.ui.current_values[i] == value:
                        found_value_index = i
                        value_found = True
                        break
        else:
            if ',' in text:
                for i in range(index + 1, len(self.ui.current_values)):
                    if tuple(self.ui.current_values[i:i + len(int_values)]) == int_values:
                        found_value_index = i
                        value_found = True
                        break
            else:
                for i in range(index + 1, len(self.ui.current_values)):
                    if self.ui.current_values[i] == value:
                        found_value_index = i
                        value_found = True
                        break

        if not value_found:
            QMessageBox.warning(self.ui, "Warning", "No matching value was found.")
            return

        selection_model = self.ui.table_view.selectionModel()
        selection_model.clearSelection()

        self.ui.mode2d.highlight_text(found_value_index - self.ui.shift_count, True)
        self.ui.mode2d.text_to_2d(self.ui)

    def edit_pasted_values(self):
        clipboard_text = QApplication.clipboard().text()
        if not '\t' in clipboard_text:
            self.find_entry.setText(clipboard_text)
            return
        values = clipboard_text.strip().replace('\r\n', '\n').replace('\t', '\n').split('\n')
        try:
            new_text = ""
            for i in range(len(values)):
                new_text += f"{int(values[i])}, " if i < len(values) - 1 else str(int(values[i]))
        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Please enter valid numbers!")
            return

        self.find_entry.setText(new_text)