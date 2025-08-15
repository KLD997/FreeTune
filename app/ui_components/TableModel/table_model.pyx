# cython: language_level=3
from PyQt6.QtCore import (
    Qt, QAbstractTableModel, QModelIndex
)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMessageBox

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.linols = parent
        self._data = [list(row) for row in data]
        self._vertical_header_labels = []
        self.undo_stack = []
        self.redo_stack = []

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index: QModelIndex, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return f"{value:05}" if value is not None else ""

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.ForegroundRole:
            color = self.linols.text_addons.highlight_difference(value, index.row(), index.column())
            if color == "blue":
                return QColor(Qt.GlobalColor.blue)
            elif color == "red":
                return QColor(Qt.GlobalColor.red)
            elif color == "default":
                return QColor(Qt.GlobalColor.white)

        if role == Qt.ItemDataRole.BackgroundRole: # highlight user maps
            index = (index.row() * self.linols.columns) + index.column()

            if self.linols.map_list_counter > 0:
                # user creted maps
                for i in range(len(self.linols.start_index_maps)):
                    down_limit = self.linols.start_index_maps[i] + self.linols.shift_count
                    up_limit = self.linols.end_index_maps[i] + self.linols.shift_count
                    if down_limit <= index <= up_limit:
                        return QColor(133, 215, 242, 150) # light blue

            # potential maps
            for i in range(len(self.linols.potential_maps_start)):
                down_limit = self.linols.potential_maps_start[i]
                up_limit = self.linols.potential_maps_end[i]
                if down_limit <= index <= up_limit:
                    return QColor(1, 133, 123, 150) # teal green

    def setData(self, index: QModelIndex, value, role):
        if role == Qt.ItemDataRole.EditRole:
            row, col = index.row(), index.column()
            try:
                new_value = int(value)
                old_value = self._data[row][col]
                if (new_value < 0) or (new_value > 65535) or old_value is None:
                    if old_value is None:
                        self._data[row][col]
                    else:
                        self._data[row][col] = self.linols.text_addons.revert_value(row, col)
                else:
                    self._data[row][col] = new_value
                    self.redraw_canvas_2d(row, col, new_value)
                self.undo_stack.append((row, col, old_value))
                self.redo_stack.clear()
                self.dataChanged.emit(index, index)
            except ValueError:
                return False
        return True

    def redraw_canvas_2d(self, row, col, value):
        self.linols.current_values = list(self.linols.current_values)
        index = (row * self.linols.columns) + col

        self.linols.current_values[index] = value

        self.linols.sync_2d_scroll = True
        self.linols.mode2d.draw_canvas(self.linols)

    def flags(self, index: QModelIndex):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def set_data(self, data):
        self._data = [list(row) for row in data]
        self.layoutChanged.emit()

    def setVerticalHeaderLabels(self, labels):
        self._vertical_header_labels = labels
        self.headerDataChanged.emit(Qt.Orientation.Vertical, 0, self.rowCount() - 1)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Vertical:
                return self._vertical_header_labels[section] if section < len(self._vertical_header_labels) else ""
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def get_all_data(self):
        return self._data

    def undo_changes(self):
        if not self.linols.file_path:
            QMessageBox.warning(self.linols, "Warning", "No file is currently open. Please open a file first.")
            return

        if not self.undo_stack:
            return

        row, col, old_value = self.undo_stack.pop()

        current_value = self._data[row][col]
        self.redo_stack.append((row, col, current_value))

        self._data[row][col] = old_value

        index = self.index(row, col)
        self.dataChanged.emit(index, index)

    def redo_changes(self):
        if not self.linols.file_path:
            QMessageBox.warning(self.linols, "Warning", "No file is currently open. Please open a file first.")
            return

        if not self.redo_stack:
            return

        row, col, old_value = self.redo_stack.pop()

        current_value = self._data[row][col]
        self.undo_stack.append((row, col, current_value))

        self._data[row][col] = old_value

        index = self.index(row, col)
        self.dataChanged.emit(index, index)
