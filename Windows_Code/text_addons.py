from PyQt6.QtWidgets import QMessageBox, QApplication, QTableView, QFileDialog
import time
import struct

class TextAddons:
    def __init__(self, ui):
        self.ui = ui
        self.time_col = 0
        self.time_shift = 0

    def revert_value(self, row, col):
        new = self.ui.unpacked[(row * self.ui.columns) + col]
        QMessageBox.warning(self.ui, "Invalid Number!", "You have entered an invalid number!")
        return new

    def highlight_difference(self, new_value, row, col):
        index = (row * self.ui.columns) + col
        if len(self.ui.unpacked) - 1 <= index:
            return "default"
        ori_value = self.ui.unpacked[index - self.ui.shift_count]
        if new_value is None:
            return None
        if new_value > ori_value:
            return "red"
        elif new_value < ori_value:
            return "blue"
        else:
            return "default"

    def on_selection(self):
        self.update_selected_count()
        self.update_ori_label()

    def update_selected_count(self):
        selection_model = self.ui.table_view.selectionModel()
        selected_indexes_count = len(selection_model.selectedIndexes())

        if selected_indexes_count > 2500:
            selection_model.clearSelection()
            selected_indexes_count = len(selection_model.selectedIndexes())

        self.ui.sel_label.setText(f"Selected: {selected_indexes_count}")

    def update_ori_label(self):
        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if len(selected_indexes) == 1:
            selected_index = selected_indexes[0]
            row = selected_index.row()
            col = selected_index.column()
            current_item = int(selected_index.data())
            index = (row * self.ui.columns) + col
            if index <= len(self.ui.unpacked):
                ori_value = self.ui.unpacked[index - self.ui.shift_count]
                self.ui.value_label.setText(f"Ori: {ori_value:05}")
                if current_item != 0 and ori_value != 0:
                    percentage_change = min(((current_item / ori_value) - 1) * 100, 999.99)
                    self.ui.difference_label.setText(f"{current_item - ori_value} ({percentage_change:.2f}%)")
                else:
                    if current_item == ori_value:
                        self.ui.difference_label.setText(f"0 (0.00%)")
                    else:
                        self.ui.difference_label.setText(f"{current_item - ori_value} (100.00%)")
            else:
                self.ui.value_label.setText("Ori: 00000")
                self.ui.difference_label.setText(f"0 (0.00%)")
        else:
            self.ui.value_label.setText("Ori: 00000")
            self.ui.difference_label.setText(f"0 (0.00%)")

    def copy_hex_address(self):
        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        selected_index = selected_indexes[0]
        row = selected_index.row()
        col = selected_index.column()

        index = (row * self.ui.columns + col) * 2

        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(f"{index:06X}")

    def copy_values(self, maps):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        if not maps:
            if not self.check_selection_rectangle() and not self.check_selection_consecutive():
                QMessageBox.warning(self.ui, "Warning", "Data selection is not correct!")
                return None
        else:
            if not self.check_selection_consecutive():
                QMessageBox.warning(self.ui, "Warning", "Data selection is not correct!")
                return False

        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        last_row = -1 # for storing previous row

        clipboard = QApplication.clipboard()
        clipboard.clear()

        text_values = ""

        for item in selected_indexes:
            row = item.row() # current row
            col = item.column() # current column

            index = (row * self.ui.columns) + col
            value = str(self.ui.current_values[index])

            if last_row == -1:
                text_values += value
            elif row == last_row:
                text_values += '\t' + value
            else:
                text_values += '\n' + value

            last_row = row

        clipboard.setText(text_values)

        if maps:
            return True

    def check_selection_rectangle(self):
        selection_model = self.ui.table_view.selectionModel()  # get all selected items
        selected_indexes = selection_model.selectedIndexes()  # all selected items

        if len(selected_indexes) < 1 or len(selected_indexes) > 1200:
            return False

        last_row = selected_indexes[0].row()
        start_col = selected_indexes[0].column()

        for i in range(1, len(selected_indexes)):
            row = selected_indexes[i].row()
            col = selected_indexes[i].column()

            if last_row != row and not last_row + 1 == row:
                return False

            if last_row != row and start_col != col:
                return False


            last_row = row

        return True

    def check_selection_consecutive(self):
        selection_model = self.ui.table_view.selectionModel()  # get all selected items
        selected_indexes = selection_model.selectedIndexes()  # all selected items

        if len(selected_indexes) < 1 or len(selected_indexes) > 1200:
            return False

        last_row = selected_indexes[0].row()
        start_col = selected_indexes[0].column()

        for i in range(1, len(selected_indexes)):
            row = selected_indexes[i].row()
            col = selected_indexes[i].column()

            if last_row != row and not last_row + 1 == row:
                return False

            if start_col + 1 == self.ui.columns:
                start_col = 0
            else:
                start_col += 1

            if col != start_col:
                return False

            last_row = row

        return True

    def check_valid_data(self, clipboard_text ,values, col_ori, row_start, col_start):
        try:
            entered_new_line = False
            x = 0
            for i in range(len(clipboard_text)): # insert data
                if values[row_start][col_start] is None:
                    raise IndexError
                if clipboard_text[i] == '\t':
                    x += 1
                    if col_start + 1 >= self.ui.columns:
                        row_start += 1
                        col_start = 0
                        entered_new_line = True
                    else:
                        col_start += 1

                if clipboard_text[i] == '\n':
                    x += 1
                    if not entered_new_line:
                        row_start += 1
                    else:
                        entered_new_line = False

                    col_start = col_ori

        except IndexError:
            QMessageBox.warning(self.ui, "Warning", "Data cannot be pasted!")
            return False

        return True

    def paste_values(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        selection_model = self.ui.table_view.selectionModel() # get all selected items
        selected_indexes = selection_model.selectedIndexes() # all selected items

        first_item = selected_indexes[0] # first selected item
        row_ori = first_item.row() # current row
        col_ori = first_item.column() # current column

        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text() # get text from clipboard

        if clipboard_text[-1] == '\n':
            clipboard_text = clipboard_text[:-1]

        values_clipboard = clipboard_text.strip().split() # get values, type -> string

        if len(values_clipboard) > 800:
            QMessageBox.warning(self.ui, "Warning", "Too much data!")
            return

        for i in range(len(values_clipboard)):
            try:
                int(values_clipboard[i])
            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Data is not correct!")
                return

        x = 0 # clipboard values counter

        values = self.ui.model.get_all_data()

        row_start = row_ori
        col_start = col_ori

        entered_new_line = False

        if not self.check_valid_data(clipboard_text ,values, col_ori, row_start, col_start):
            return

        try:
            for i in range(len(clipboard_text)): # insert data
                if values[row_start][col_start] is None:
                    raise IndexError
                if clipboard_text[i] == '\t':
                    values[row_start][col_start] = int(values_clipboard[x])
                    x += 1
                    if col_start + 1 >= self.ui.columns:
                        row_start += 1
                        col_start = 0
                        entered_new_line = True
                    else:
                        col_start += 1

                if clipboard_text[i] == '\n':
                    values[row_start][col_start] = int(values_clipboard[x])
                    x += 1
                    if not entered_new_line:
                        row_start += 1
                    else:
                        entered_new_line = False

                    col_start = col_ori

        except IndexError:
            QMessageBox.warning(self.ui, "Warning", "Data cannot be pasted!")
            return

        # add last values
        values[row_start][col_start] = int(values_clipboard[x])

        # reinsert data
        self.ui.current_values = []

        for i in range(self.ui.shift_count):
            self.ui.current_values.append(None)

        for row in values:
            for col in row:
                if col is not None:
                    self.ui.current_values.append(col)

        rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                range(0, len(self.ui.current_values) - self.ui.columns, self.ui.columns)]  # get values by rows

        remaining_elements = len(self.ui.current_values) % self.ui.columns  # last row offset

        if remaining_elements:
            last_row = list(self.ui.current_values[-remaining_elements:]) + [None] * (
                    self.ui.columns - remaining_elements)  # last row values
            rows.append(last_row)

        self.ui.model.set_data(rows)
        self.ui.model.layoutChanged.emit()

        from text_view import TextView
        text_view = TextView(self.ui)

        text_view.set_labels_y_axis()
        text_view.set_column_width()

        index_sel = self.ui.model.index(row_ori, col_ori)
        self.ui.table_view.scrollTo(index_sel, QTableView.ScrollHint.PositionAtCenter)

    def adjust_columns(self, mode):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        current_time = time.time()
        if self.time_col + 0.5 >= current_time:
            return

        self.time_col = current_time

        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if selected_indexes:
            current_row = selected_indexes[0].row()
            current_col = selected_indexes[0].column()
            index = (current_row * self.ui.columns) + current_col
        else:
            index = self.ui.table_view.get_first_visible_index()

        if mode == "+" and self.ui.columns < 50:
            self.ui.columns += 1
        elif mode == "-" and self.ui.columns > 1:
            self.ui.columns -= 1
        else:
            return

        if self.ui.columns == self.ui.shift_count:
            self.ui.shift_count -= 1
            self.ui.entry_shift.setText(f"Shift: {self.ui.shift_count:02}")

        values = self.ui.model.get_all_data()

        self.ui.current_values = []

        for i in range(self.ui.shift_count):
            self.ui.current_values.append(None)

        for row in values:
            for col in row:
                if col is not None:
                    self.ui.current_values.append(col)

        rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                range(0, len(self.ui.current_values), self.ui.columns)]

        if len(rows[-1]) < self.ui.columns:
            rows[-1].extend([None] * (self.ui.columns - len(rows[-1])))

        self.ui.model.set_data(rows)
        self.ui.model.layoutChanged.emit()

        from text_view import TextView
        text_view = TextView(self.ui)
        text_view.set_labels_y_axis()
        text_view.set_column_width()

        self.ui.entry_col.setText(f"Columns: {self.ui.columns:02}")

        if self.ui.current_values[index] is None:
            while index < len(self.ui.current_values) and self.ui.current_values[index] is None:
                index += 1

        self.ui.mode2d.highlight_text(index - self.ui.shift_count, True)

    def shift_values(self, mode):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        time_shift_now = time.time()

        if self.time_shift + 0.5 >= time_shift_now:
            return

        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if selected_indexes:
            current_row = selected_indexes[0].row()
            current_col = selected_indexes[0].column()
            index = (current_row * self.ui.columns) + current_col
        else:
            index = self.ui.table_view.get_first_visible_index()

        if mode == "+" and self.ui.shift_count + 1 < self.ui.columns:
            self.ui.shift_count += 1
            for i in range(len(self.ui.potential_maps_start)):
                self.ui.potential_maps_start[i] += 1
                self.ui.potential_maps_end[i] += 1
        elif mode == "-" and self.ui.shift_count >= 1:
            self.ui.shift_count -= 1
            for i in range(len(self.ui.potential_maps_start)):
                self.ui.potential_maps_start[i] -= 1
                self.ui.potential_maps_end[i] -= 1
        else:
            return

        values = self.ui.model.get_all_data()

        self.ui.current_values = []

        for i in range(self.ui.shift_count):
            self.ui.current_values.append(None)

        for row in values:
            for col in row:
                if col is not None:
                    self.ui.current_values.append(col)

        rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                range(0, len(self.ui.current_values) - self.ui.columns, self.ui.columns)]  # get values by rows

        remaining_elements = len(self.ui.current_values) % self.ui.columns  # last row offset

        if remaining_elements:
            last_row = list(self.ui.current_values[-remaining_elements:]) + [None] * (
                    self.ui.columns - remaining_elements)  # last row values
            rows.append(last_row)

        self.ui.model.set_data(rows)
        self.ui.model.layoutChanged.emit()

        from text_view import TextView
        text_view = TextView(self.ui)

        text_view.set_labels_y_axis()
        text_view.set_column_width()

        self.ui.entry_shift.setText(f"Shift: {self.ui.shift_count:02}")

        if self.ui.current_values[index] is None:
            while index < len(self.ui.current_values) and self.ui.current_values[index] is None:
                index += 1
            index -= 1

        self.ui.mode2d.highlight_text(index - self.ui.shift_count + (1 if mode == "+" else -1), True)

    def on_tab_changed(self, index):
        if index == 0:
            self.ui.tab1_selected = True
        else:
            self.ui.tab1_selected = False
        if index == 1:
            self.ui.disable_2d_canvas = False
            self.ui.sync_2d_scroll = False
            self.ui.mode2d.draw_canvas(self.ui)
        else:
            self.ui.disable_2d_canvas = True
            self.ui.sync_2d_scroll = True
        if index == 2:
            self.ui.tk_win_manager.open_tkinter_window()
            self.ui.focused_3d_tab = True
        else:
            self.ui.tk_win_manager.kill_tkinter_window()
            self.ui.focused_3d_tab = False

    def import_file(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return
        import_file_path, selected_filter = QFileDialog.getOpenFileName(self.ui, "Open File")
        if not import_file_path:
            QMessageBox.warning(self.ui, "Warning", "No file for importing is currently open. "
                                                 "Please open a file for importing first.")
            return

        with open(import_file_path, 'rb') as file:
            content = file.read()
            if self.ui.low_high:
                values = struct.unpack('<' + 'H' * (len(content) // 2), content)
            else:
                values = struct.unpack('>' + 'H' * (len(content) // 2), content)

        self.ui.current_values = []

        for i in range(self.ui.shift_count):
            self.ui.current_values.append(None)

        for item in values:
            if item is not None:
                self.ui.current_values.append(item)

        rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                range(0, len(self.ui.current_values) - self.ui.columns, self.ui.columns)]  # get values by rows

        remaining_elements = len(self.ui.current_values) % self.ui.columns  # last row offset

        if remaining_elements:
            last_row = list(self.ui.current_values[-remaining_elements:]) + [None] * (
                    self.ui.columns - remaining_elements)  # last row values
            rows.append(last_row)

        self.ui.model.set_data(rows)
        self.ui.model.layoutChanged.emit()

        from text_view import TextView
        text_view = TextView(self.ui)

        text_view.set_labels_y_axis()
        text_view.set_column_width()

    def set_text(self, int_value):
        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self.ui, "Warning", "There is no values selected!")
            return

        temp_list = list(self.ui.current_values)

        for item in selected_indexes:
            row = item.row()
            col = item.column()

            index = (row * self.ui.columns) + col

            temp_list[index] = int(int_value)

        self.ui.current_values = temp_list

        rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                range(0, len(self.ui.current_values) - self.ui.columns, self.ui.columns)]  # get values by rows

        remaining_elements = len(self.ui.current_values) % self.ui.columns  # last row offset

        if remaining_elements:
            last_row = list(self.ui.current_values[-remaining_elements:]) + [None] * (
                    self.ui.columns - remaining_elements)  # last row values
            rows.append(last_row)

        self.ui.model.set_data(rows)
        self.ui.model.layoutChanged.emit()

        self.ui.text_view_.set_labels_y_axis()
        self.ui.text_view_.set_column_width()

    def increase_selected_text(self, int_value):
        try:
            selection_model = self.ui.table_view.selectionModel()
            selected_indexes = selection_model.selectedIndexes()
            if not selected_indexes:
                QMessageBox.warning(self.ui, "Warning", "There is no values selected!")
                return

            temp_list = list(self.ui.current_values)

            for item in selected_indexes:
                row = item.row()
                col = item.column()

                index_elements = (row * self.ui.columns) + col

                new_value = int_value + self.ui.current_values[index_elements]

                if 0 > new_value or new_value > 65535:
                    raise ValueError

                index = (row * self.ui.columns) + col

                temp_list[index] = int(new_value)

            self.ui.current_values = temp_list

            rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                    range(0, len(self.ui.current_values) - self.ui.columns, self.ui.columns)]  # get values by rows

            remaining_elements = len(self.ui.current_values) % self.ui.columns  # last row offset

            if remaining_elements:
                last_row = list(self.ui.current_values[-remaining_elements:]) + [None] * (
                        self.ui.columns - remaining_elements)  # last row values
                rows.append(last_row)

            self.ui.model.set_data(rows)
            self.ui.model.layoutChanged.emit()

            self.ui.text_view_.set_labels_y_axis()
            self.ui.text_view_.set_column_width()

        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Please enter a valid number.")

    def increase_selected_text_per(self, float_value):
        try:
            percentage_increase = float_value / 100.0

            selection_model = self.ui.table_view.selectionModel()
            selected_indexes = selection_model.selectedIndexes()
            if not selected_indexes:
                QMessageBox.warning(self.ui, "Warning", "There is no values selected!")
                return

            temp_list = list(self.ui.current_values)

            for item in selected_indexes:
                row = item.row()
                col = item.column()

                index = (row * self.ui.columns) + col

                current_value = self.ui.current_values[index]
                increase_value = int(current_value * percentage_increase)

                new_value = current_value + increase_value

                if 0 > new_value or new_value > 65535:
                    raise ValueError


                temp_list[index] = new_value

            self.ui.current_values = temp_list

            rows = [self.ui.current_values[i:i + self.ui.columns] for i in
                    range(0, len(self.ui.current_values) - self.ui.columns, self.ui.columns)]  # get values by rows

            remaining_elements = len(self.ui.current_values) % self.ui.columns  # last row offset

            if remaining_elements:
                last_row = list(self.ui.current_values[-remaining_elements:]) + [None] * (
                        self.ui.columns - remaining_elements)  # last row values
                rows.append(last_row)

            self.ui.model.set_data(rows)
            self.ui.model.layoutChanged.emit()

            self.ui.text_view_.set_labels_y_axis()
            self.ui.text_view_.set_column_width()

        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Please enter a valid number.")

    def open_find_dialog(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return
        from custom_dialogs.find_dialog import FindDialog
        dialog = FindDialog(self.ui)
        dialog.exec()

    def open_value_dialog(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return
        from custom_dialogs.value_dialog import ValueDialog
        dialog = ValueDialog(self.ui)
        dialog.exec()

    def open_hex_address_dialog(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return
        from custom_dialogs.hex_address_dialog import HexAddressDialog
        dialog = HexAddressDialog(self.ui)

        dialog.exec()

    def open_difference_dialog(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return
        from custom_dialogs.difference_dialog import DifferenceDialog
        dialog = DifferenceDialog(self.ui)
        dialog.exec()