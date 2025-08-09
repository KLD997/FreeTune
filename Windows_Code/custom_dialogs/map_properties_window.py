import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, \
    QStyledItemDelegate, QWidget
from PyQt6.QtCore import Qt

class CenteredItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter

    def paint(self, painter, option, index):
        nudged_rect = option.rect.adjusted(-9, 0, -9, 0)
        option.rect = nudged_rect
        super().paint(painter, option, index)

class MapProperties(QDialog):
    def __init__(self, ui):
        super().__init__(ui)
        self.ui = ui

        self.setWindowTitle("Map Properties")
        self.setFixedSize(250, 200)
        self.setStyleSheet("background-color: #333;")

        self.setWindowIcon(self.ui.logo_icon)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.form_container = QWidget()
        self.form_container.setFixedSize(250, 200)

        self.setup_ui()

        outer_layout.addWidget(self.form_container)

        self.insert_all_info()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 10, 15, 10)

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
                min-width: 65px;
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

        button_style_op = """
            QPushButton {
                background-color: #444;
                color: white;
                font-family: 'Roboto', sans-serif;
                font-size: 12px;
                font-weight: 650;
                padding: 6px;
                border: none;
                border-radius: 5px;
                min-width: 10px;
                margin-left: 8px;
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

        label_style = """
            border: 0;
            color: white;
            font-family: 'Roboto';
            font-size: 15px;
            font-weight: 650;
            background: transparent;
        """

        entry_style = """
            border: 2px;
            border-radius: 5px;
            font-family: 'Roboto';
            font-size: 15px;
            font-weight: 650;
            background-color: #555;
            height: 25px;
            width: 50px;
            color: white;
        """

        # Name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setStyleSheet(label_style)
        self.name_entry = QLineEdit()
        self.name_entry.setStyleSheet(entry_style)
        self.name_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_entry.setFixedWidth(165)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_entry)
        main_layout.addLayout(name_layout)

        # Size dropdown
        size_layout = QHBoxLayout()
        size_label = QLabel("Size:")
        size_label.setStyleSheet(label_style)
        self.size_menu = QComboBox()
        self.size_menu.setStyleSheet(entry_style)
        self.size_menu.setFixedWidth(165)
        self.size_menu.setEditable(True)
        self.size_menu.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_menu.lineEdit().setReadOnly(True)
        self.size_menu.setItemDelegate(CenteredItemDelegate(self.size_menu))
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_menu)
        main_layout.addLayout(size_layout)

        # Factor field
        factor_layout = QHBoxLayout()
        factor_label = QLabel("Factor:")
        factor_label.setStyleSheet(label_style)
        self.factor_entry = QLineEdit()
        self.factor_entry.setStyleSheet(entry_style)
        self.factor_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.factor_entry.setFixedWidth(165)
        factor_layout.addWidget(factor_label)
        factor_layout.addWidget(self.factor_entry)
        main_layout.addLayout(factor_layout)

        # Precision controls
        precision_layout = QHBoxLayout()
        precision_label = QLabel("Decimals:")
        precision_label.setStyleSheet(label_style)
        self.precision_entry = QLineEdit()
        self.precision_entry.setReadOnly(True)
        self.precision_entry.setStyleSheet(entry_style)
        self.precision_entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        precision_plus = QPushButton("+")
        precision_plus.setStyleSheet(button_style_op)
        precision_minus = QPushButton("-")
        precision_minus.setStyleSheet(button_style_op)

        precision_plus.clicked.connect(lambda: self.precision_increase("+"))
        precision_minus.clicked.connect(lambda: self.precision_increase("-"))

        precision_layout.addWidget(precision_label)
        precision_layout.addWidget(self.precision_entry)
        precision_layout.addWidget(precision_plus)
        precision_layout.addWidget(precision_minus)
        main_layout.addLayout(precision_layout)

        # Apply button
        apply_button = QPushButton("Apply")
        apply_button.setStyleSheet(button_style)
        apply_button.clicked.connect(self.apply_changes)
        main_layout.addWidget(apply_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.form_container.setLayout(main_layout)

    def insert_all_info(self):
        maps = self.ui.maps

        if not os.path.exists(maps.file_path):
            return

        file_path = maps.file_path
        index = maps.last_map_index

        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Warning", "Please open a map first!")
            self.close()
            return

        with open(file_path, 'r') as file:
            content = file.read().split('\n')
            self.map_name = content[index * 10]
            self.map_size = content[(index * 10) + 3]
            map_factor = content[(index * 10) + 4]
            map_precision = content[(index * 10) + 5]

            self.name_entry.setText(self.map_name)
            self.size_menu.clear()
            new_sizes = self.calculate_possible_size()
            self.size_menu.addItems(new_sizes)
            self.size_menu.setCurrentText(self.map_size)

            self.factor_entry.setText(f"{map_factor}")
            self.precision_entry.setText(f"{map_precision}")

    def calculate_possible_size(self):
        size = self.map_size.split('x')
        col = int(size[0])
        row = int(size[1])
        data = col * row

        factors = []
        for i in range(1, 42):
            if data % i == 0:
                factors.append(i)
                factors.append(data // i)

        new_sizes = []
        for i in range(0, len(factors), 2):
            new_sizes.append(f"{factors[i]}x{factors[i + 1]}")
        return new_sizes

    def apply_changes(self):
        maps = self.ui.maps

        file_path = maps.file_path
        index = maps.last_map_index

        new_map_name = self.name_entry.text()
        new_size = self.size_menu.currentText()
        try:
            new_map_factor = float(self.factor_entry.text())
            if not (0 <= new_map_factor <= 1):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter valid map factor!")
            return

        try:
            new_map_precision = int(self.precision_entry.text())
            if not (0 <= new_map_precision <= 6):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter valid precision!")
            return

        with open(file_path, 'r') as file:
            content = file.read().split('\n')
            for i in range(0, len(content), 10):
                if content[i] == new_map_name and i // 10 != maps.last_map_index:
                    QMessageBox.warning(self, "Warning", "You cannot use the already used name!")
                    return

        maps.write_map()

        index *= 10
        content[index] = new_map_name
        content[index + 3] = new_size
        content[index + 4] = str(new_map_factor)
        content[index + 5] = str(new_map_precision)

        with open(file_path, 'w') as file:
            for i in range(len(content)):
                file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])

        self.ui.map_list.takeItem(maps.last_map_index)

        self.ui.map_list.insertItem(maps.last_map_index, new_map_name)

        maps.update_3d_from_text()
        self.ui.dialog_terminate = False
        self.close()

    def precision_increase(self, mode):
        value = int(self.precision_entry.text())

        if mode == "+" and value + 1 <= 6:
            value += 1
        if mode == "-" and value - 1 >= 0:
            value -= 1

        self.precision_entry.setText(str(value))
