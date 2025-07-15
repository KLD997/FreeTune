import struct
import os
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QFileDialog


class TextView:
    def __init__(self, ui):
        self.ui = ui

    def open_file(self):
        file_path, selected_filter = QFileDialog.getOpenFileName(self.ui, "Open File")
        if file_path:
            self.ui.file_path = file_path
        else:
            return

        if self.ui.file_path:
            with open(self.ui.file_path, 'rb') as file:
                content = file.read()
                if len(content) % 2 != 0:
                    QMessageBox.warning(self.ui, "Error", "Please open a valid file!")
                    return
                if self.ui.low_high:
                    self.ui.unpacked = struct.unpack('<' + 'H' * (len(content) // 2), content)
                    self.ui.btn_lo_hi.setEnabled(False)
                    self.ui.btn_hi_lo.setEnabled(True)
                else:
                    self.ui.unpacked = struct.unpack('>' + 'H' * (len(content) // 2), content)
                    self.ui.btn_lo_hi.setEnabled(True)
                    self.ui.btn_hi_lo.setEnabled(False)

                self.ui.current_values = self.ui.unpacked

                self.ui.columns = 20
                self.ui.shift_count = 0

                self.ui.entry_col.setText(f"Columns: {self.ui.columns:02}")
                self.ui.entry_shift.setText(f"Shift: {self.ui.shift_count:02}")

                self.rows = [self.ui.unpacked[i:i + self.ui.columns] for i in
                             range(0, len(self.ui.unpacked) - self.ui.columns, self.ui.columns)] # get values by rows

                remaining_elements = len(self.ui.unpacked) % self.ui.columns # last row offset

                if remaining_elements:
                    last_row = list(self.ui.unpacked[-remaining_elements:]) + [None] * (
                                self.ui.columns - remaining_elements) # last row values
                    self.rows.append(last_row)

                from ui import CustomTableView, QTableModel
                CustomTableView(self.ui)
                QTableModel(self.rows, self.ui)

                self.ui.model.set_data(self.rows) # set values
                self.ui.model.layoutChanged.emit() # update table view

                self.set_column_width()
                self.set_labels_y_axis()

                # reset variables
                self.ui.differences = []
                self.ui.ori_values = []
                self.ui.map_list.clear()
                self.ui.map_list_counter = 0
                self.ui.start_index_maps = []
                self.ui.end_index_maps = []
                self.ui.maps_names = []
                self.ui.maps.last_map_index = 0

                self.ui.maps.start_potential_map_search(False)

                from Module_2D import Mode2D
                self.mode2d = Mode2D(self)
                self.mode2d.draw_canvas(self.ui)

                self.ui.mode3d.set_default()

    def set_labels_y_axis(self):
        labels = []
        for i in range(self.ui.model.rowCount()):
            value = (i * self.ui.model.columnCount()) * 2
            value = f"{value:06X}"
            labels.append(value)

        self.ui.model.setVerticalHeaderLabels(labels) # set the vertical header

    def set_column_width(self, width=60): # changes size of every column
        for col in range(self.ui.columns):
            self.ui.table_view.setColumnWidth(col, width)

    def ask_change_display_mode(self, mode):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        msg_box = QMessageBox(self.ui)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setWindowTitle("Change Display Mode")
        msg_box.setText("Do you really want to change the display mode?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)

        response = msg_box.exec()

        if response == QMessageBox.StandardButton.Yes:
            self.change_display_mode(mode)

    def change_display_mode(self, mode):
        unpacked_byte_change = []

        for value in self.ui.unpacked:
            low = value & 0xFF
            high = (value >> 8) & 0xFF
            combined = (low * 256) + high
            unpacked_byte_change.append(combined)

        current_values_byte_change = []
        for value in self.ui.current_values:
            if value is None:
                continue
            low = value & 0xFF
            high = (value >> 8) & 0xFF
            combined = (low * 256) + high
            current_values_byte_change.append(combined)

        self.ui.unpacked = unpacked_byte_change
        self.ui.current_values = current_values_byte_change

        if mode == "low_high":
            self.ui.low_high = True
            self.ui.btn_lo_hi.setEnabled(False)
            self.ui.btn_hi_lo.setEnabled(True)

        elif mode == "high_low":
            self.ui.low_high = False
            self.ui.btn_lo_hi.setEnabled(True)
            self.ui.btn_hi_lo.setEnabled(False)

        rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                range(0, len(self.ui.current_values) - self.ui.columns, self.ui.columns)]  # get values by rows

        remaining_elements = len(self.ui.current_values) % self.ui.columns  # last row offset

        if remaining_elements:
            last_row = list(self.ui.current_values[-remaining_elements:]) + [None] * (
                    self.ui.columns - remaining_elements)  # last row values
            rows.append(last_row)

        self.ui.model.set_data(rows)
        self.ui.model.layoutChanged.emit()

        self.set_labels_y_axis()
        self.set_column_width()

    def save_file(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        values = self.ui.model.get_all_data()
        current_values = []
        for row in values:
            for col in row:
                if col is not None:
                    current_values.append(col)

        file_name = self.ui.last_file_name

        last_file_dir = ""

        if not self.ui.last_file_name:
            manufacturer, ok1 = QInputDialog.getText(self.ui, "Input", "Enter Manufacturer:")
            model, ok2 = QInputDialog.getText(self.ui, "Input", "Enter Model:")
            modification, ok3 = QInputDialog.getText(self.ui, "Input", "Enter Modification:")

            if not (ok1 and ok2 and ok3 and manufacturer and model and modification):
                QMessageBox.warning(self.ui, "Warning", "Manufacturer, Model, and Modification are required.")
                return

            file_name = f"LinOLS_{manufacturer}_{model}_{modification}.bin"
            user_directory = os.path.expanduser("~")
            file_name = os.path.join(user_directory, file_name)
            self.ui.last_file_name = file_name

            new_file = True
        else:
            msg_box = QMessageBox(self.ui)
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Save with Previous File Name")
            msg_box.setText("Would you like to save the file with the previous file name?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)

            response = msg_box.exec()

            if response == QMessageBox.StandardButton.No:
                manufacturer, ok1 = QInputDialog.getText(self.ui, "Input", "Enter Manufacturer:")
                model, ok2 = QInputDialog.getText(self.ui, "Input", "Enter Model:")
                modification, ok3 = QInputDialog.getText(self.ui, "Input", "Enter Modification:")

                if not (ok1 and ok2 and ok3 and manufacturer and model and modification):
                    QMessageBox.warning(self.ui, "Warning", "Manufacturer, Model, and Modification are required.")
                    return

                last_file_dir = self.ui.last_file_name
                file_name = f"LinOLS_{manufacturer}_{model}_{modification}.bin"
                last_dir = self.ui.last_file_name[self.ui.last_file_name.rfind('/') + 1:]
                file_name = os.path.join(last_dir, file_name)
                self.ui.last_file_name = file_name

                new_file = True
            else:
                new_file = False

        try:
            file_path = ""

            if new_file:
                file_path, selected_filter = QFileDialog.getSaveFileName(self.ui, "Save File", file_name, "Binary Files (*.bin);;All Files (*)")

                if not file_path:
                    QMessageBox.information(self.ui, "Info", "File save canceled.")
                    if last_file_dir:
                        self.ui.last_file_name = last_file_dir
                    return

            if self.ui.low_high:
                content_to_write = b''.join(struct.pack('<H', int(value)) for value in current_values)
            else:
                content_to_write = b''.join(struct.pack('>H', int(value)) for value in current_values)

            if file_path:
                with open(file_path, 'wb') as file:
                    self.ui.last_file_name = file_path
                    file.write(content_to_write)
            else:
                with open(self.ui.last_file_name, 'wb') as file:
                    file.write(content_to_write)

            QMessageBox.information(self.ui, "Success", f"File saved successfully at {self.ui.last_file_name}.")
        except Exception as e:
            QMessageBox.warning(self.ui, "Error", f"Error saving file: {e}")