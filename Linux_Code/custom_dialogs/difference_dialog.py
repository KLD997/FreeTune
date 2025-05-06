from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont


class DifferenceDialog(QDialog):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.setWindowTitle("Difference Dialog")
        self.setFixedSize(600, 450)
        self.setStyleSheet("background-color: #333; border:0;")

        screen = QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        x = (screen_rect.width() - self.width()) // 2
        y = (screen_rect.height() - self.height()) // 2
        self.move(x, y)

        self.ui.dialog_terminate = False

        diff_list_box_widget = DiffListBox(self)
        diff_list_box_widget.setStyleSheet("""
            QTableView {
                background-color: #333;
            }
            QTableView::item:selected {
                background-color: #5b9bf8;
                color: white;
            }
            QHeaderView::section {
                background-color: #363636;
                color: white;
            } 
        """)

        font = QFont("Cantarell", 11)
        diff_list_box_widget.setFont(font)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(diff_list_box_widget)

    def get_diff_data(self):
        data = []
        new_values = self.ui.current_values[self.ui.shift_count:]
        counter = 0
        for i in range(len(new_values)):
            if new_values[i] != self.ui.unpacked[i]:
                ori_val = self.ui.unpacked[i]
                new_val = new_values[i]
                hex_address = i * 2

                diff_value = self.ui.unpacked[i] - new_values[i]

                if ori_val == 0:
                    percentage_difference = 100.0
                else:
                    percentage_difference = ((new_val - ori_val) / ori_val) * 100

                    if percentage_difference > 999.0:
                        percentage_difference = 999.0

                per_diff_str = f"{round(percentage_difference, 2)}%"

                data.append([counter + 1, f"{hex_address:06X}", ori_val, new_val, diff_value, per_diff_str])
                counter += 1

        return data

class DiffListBox(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.dialog_ = parent

        layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        font = QFont("Cantarell", 10)
        self.table.horizontalHeader().setFont(font)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['No.', 'Address', 'Original', 'New Value', 'Change', 'Change %'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 90)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)

        data = self.dialog_.get_diff_data()

        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col_idx == 5:
                    item.setForeground(QColor("blue") if "-" in str(value) else QColor("red"))
                self.table.setItem(row_idx, col_idx, item)

        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.table.cellDoubleClicked.connect(self.on_row_activated)

    def on_row_activated(self, row, _col=None):
        hex_address = self.table.item(row, 1).text()
        self.find_hex(hex_address)


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            row = self.table.currentRow()
            if row >= 0:
                self.on_row_activated(row)
        else:
            super().keyPressEvent(event)

    def find_hex(self, hex_address):
        index = int(hex_address, 16)
        index = index // 2

        self.highlight_hex(index)

    def highlight_hex(self, index):
        selection_model = self.dialog_.ui.table_view.selectionModel()
        selection_model.clearSelection()

        self.dialog_.ui.mode2d.highlight_text(index, True)
        self.dialog_.ui.mode2d.text_to_2d(self.dialog_.ui)