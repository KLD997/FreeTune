from PyQt6.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton


class Factor_Dialog(QDialog):
    def __init__(self, parent=None, local_parent=None, factors=None):
        super().__init__(parent)
        self.setWindowTitle("Map Creator")
        self.setStyleSheet("background-color: #333;")
        self.setFixedSize(250, 120)
        self.ui = parent

        self.local_parent = local_parent

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()

        label = QLabel("Select a factor:")
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        self.factor_list = QListWidget()
        self.factor_list.setStyleSheet("background-color: #333; color: white;")
        layout.addWidget(self.factor_list)

        for i in range(0, len(factors), 2): # insert data
            self.factor_list.addItem(f"{factors[i]}x{int(factors[i + 1])}")

        self.factor_list.itemDoubleClicked.connect(self.factor_select) # Connect double-click event

        self.setLayout(layout)

    def factor_select(self, item):
        selected_item = self.factor_list.currentItem()
        if selected_item:
            item = selected_item.text()
            self.local_parent.size = item
            self.ui.dialog_terminate = False
        self.close()
        self.local_parent.map_name_dialog()

class Map_Name_Dialog(QDialog):
    def __init__(self, parent=None, local_parent=None):
        super().__init__(parent)
        self.setWindowTitle("Map Creator")
        self.setStyleSheet("background-color: #333;")
        self.setFixedSize(250, 120)

        self.ui = parent
        self.local_parent = local_parent

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)

        layout = QVBoxLayout()

        label = QLabel("Name your map:")
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        self.name_entry = QLineEdit()
        self.name_entry.setStyleSheet("background-color: #555; color: white;")
        layout.addWidget(self.name_entry)

        btn = QPushButton("Create")
        btn.setStyleSheet("background-color: #444; color: white;")
        layout.addWidget(btn)
        btn.clicked.connect(self.create_map)

        self.setLayout(layout)

    def create_map(self):
        self.ui.dialog_terminate = False
        self.close()
        self.local_parent.create_map(self.name_entry.text())