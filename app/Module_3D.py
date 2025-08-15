import math
import re
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QApplication, QInputDialog

class Mode3D:
    def __init__(self, ui):
        self.ui = ui
        self.map_precision = 0

    def copy_selected_3d(self):
        if not self.check_selection_rectangle_3d() and not self.check_selection_consecutive_3d():
            QMessageBox.warning(self.ui, "Warning", "Data selection is not correct!")
            return

        selected_items = self.ui.box_layout.selectedItems()

        last_row = -1 # for storing previous row

        clipboard = QApplication.clipboard()
        clipboard.clear()

        text_values = ""

        for item in selected_items:
            row = item.row() # current row
            col = item.column() # current column

            entry = self.ui.box_layout.item(row, col)
            value = entry.text()

            if last_row == -1:
                text_values += value
            elif row == last_row:
                text_values += '\t' + value
            else:
                text_values += '\n' + value

            last_row = row

        clipboard.setText(text_values)

    def check_selection_rectangle_3d(self):
        selected_items = self.ui.box_layout.selectedItems()

        if len(selected_items) < 1 or len(selected_items) > 1200:
            return False

        last_row = selected_items[0].row()
        start_col = selected_items[0].column()

        for i in range(1, len(selected_items)):
            row = selected_items[i].row()
            col = selected_items[i].column()

            if last_row != row and not last_row + 1 == row:
                return False

            if last_row != row and start_col != col:
                return False


            last_row = row

        return True

    def check_selection_consecutive_3d(self):
        selected_items = self.ui.box_layout.selectedItems()

        if len(selected_items) < 1 or len(selected_items) > 1200:
            return False

        last_row = selected_items[0].row()
        start_col = selected_items[0].column()

        for i in range(1, len(selected_items)):
            row = selected_items[i].row()
            col = selected_items[i].column()

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


    def increase_selected_text(self, int_value):
        try:
            increase_value = int_value
            selected_items = self.ui.box_layout.selectedItems()
            if not selected_items:
                return

            for i in range(len(selected_items)):
                row = selected_items[i].row()
                col = selected_items[i].column()
                entry = self.ui.box_layout.item(row, col)
                if not self.ui.map_decimal:
                    current_value = int(entry.text())
                else:
                    current_value = float(entry.text().strip())
                new_value = current_value + increase_value
                if 0 > new_value or new_value > 65535:
                    raise ValueError
                if not self.ui.map_decimal:
                    new_value_str = f"{new_value:05}"
                    entry.setText(new_value_str)
                else:
                    new_data = float(round(new_value, self.map_precision))
                    parts = str(new_data).split('.')
                    decimal_length = len(parts[1])
                    str_data = str(new_data)
                    if decimal_length < self.map_precision:
                        for x in range(self.map_precision - decimal_length):
                            str_data += "0"
                    parts = str_data.split('.')
                    entry.setText(f"{int(parts[0]):05}.{parts[1]}")

                self.check_difference(row, col)

        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Please enter a valid number.")

    def increase_selected_text_per(self, float_value):
        try:
            percentage_increase = float_value / 100.0
            selected_items = self.ui.box_layout.selectedItems()
            if not selected_items:
                return

            for i in range(len(selected_items)):
                row = selected_items[i].row()
                col = selected_items[i].column()
                entry = self.ui.box_layout.item(row, col)
                if not self.ui.map_decimal:
                    current_value = int(entry.text())
                    increase_value = int(current_value * percentage_increase)
                else:
                    current_value = float(entry.text())
                    increase_value = float(current_value * percentage_increase)
                new_value = current_value + increase_value
                if 0 > new_value or new_value > 65535:
                    raise ValueError
                if not self.ui.map_decimal:
                    new_value_str = f"{math.ceil(new_value):05}"
                    entry.setText(new_value_str)
                else:
                    new_data = float(round(math.ceil(new_value), self.map_precision))
                    parts = str(new_data).split('.')
                    decimal_length = len(parts[1])
                    str_data = str(new_data)
                    if decimal_length < self.map_precision:
                        for x in range(self.map_precision - decimal_length):
                            str_data += "0"
                    parts = str_data.split('.')
                    entry.setText(f"{int(parts[0]):05}.{parts[1]}")

                self.check_difference(row, col)

        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Please enter a valid number.")

    def set_text(self, int_value):
        try:
            selected_items = self.ui.box_layout.selectedItems()
            if not selected_items:
                return

            for i in range(len(selected_items)):
                row = selected_items[i].row()
                col = selected_items[i].column()
                entry = self.ui.box_layout.item(row, col)
                if not self.ui.map_decimal:
                    new_value = int_value
                    new_value_str = f"{new_value:05}"
                    entry.setText(new_value_str)
                else:
                    new_data = float(round(int_value, self.map_precision))
                    parts = str(new_data).split('.')
                    decimal_length = len(parts[1])
                    str_data = str(new_data)
                    if decimal_length < self.map_precision:
                        for x in range(self.map_precision - decimal_length):
                            str_data += "0"
                    parts = str_data.split('.')
                    entry.setText(f"{int(parts[0]):05}.{parts[1]}")
                self.check_difference(row, col)

        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Please enter a valid number.")

    def resize_grid(self, new_columns, new_rows, new):
        self.ui.num_columns_3d = new_columns
        self.ui.num_rows_3d = new_rows

        self.ui.box_layout.setRowCount(self.ui.num_rows_3d)
        self.ui.box_layout.setColumnCount(self.ui.num_columns_3d)

        horizontal_headers = [str(i + 1) for i in range(self.ui.num_columns_3d)]
        vertical_headers = [str(i + 1) for i in range(self.ui.num_rows_3d)]

        self.ui.box_layout.setHorizontalHeaderLabels(horizontal_headers)
        self.ui.box_layout.setVerticalHeaderLabels(vertical_headers)

        for col in range(self.ui.num_columns_3d):
            header_item = QTableWidgetItem(horizontal_headers[col])
            self.ui.box_layout.setHorizontalHeaderItem(col, header_item)

        for row in range(self.ui.num_rows_3d):
            header_item = QTableWidgetItem(vertical_headers[row])
            self.ui.box_layout.setVerticalHeaderItem(row, header_item)

        if not new:
            self.ui.original = []
            self.ui.original_x = []
            self.ui.original_y = []

            for i in range(self.ui.num_rows_3d):
                row = []
                self.ui.original_y.append(i + 1)
                for x in range(self.ui.num_columns_3d):
                    row.append(0)
                self.ui.original.append(row)

            for i in range(self.ui.num_columns_3d):
                self.ui.original_x.append(i + 1)

    def paste_data(self, maps_sel, data, row, col, new, name):
        if maps_sel:
            maps = self.ui.maps
            with open(maps.file_path, 'r') as file:
                content = file.read().split('\n')
                for i in range(len(content)):
                    if content[i] == name:
                        try:
                            map_factor = float(content[i + 4])
                            self.map_precision = int(content[i + 5])
                            x_precision = int(content[i + 7])
                            break
                        except ValueError:
                            QMessageBox.warning(self.ui, "Warning",
                                                "There is a problem with the mappack file. It appears to have been modified by an user."
                                                "\nPlease restart the application!")
                            return

            self.resize_grid(col, row, new)
            index = 0
            str_data = ""
            self.ui.map_values = []

            for i in range(row):
                for j in range(col):
                    data = list(data)
                    data[index] = int(data[index])
                    if map_factor != 1.0:
                        data[index] *= map_factor
                    self.ui.map_values.append(data[index])
                    if self.map_precision != 0:
                        new_data = float(round(data[index], self.map_precision))
                        parts = str(new_data).split('.')
                        decimal_length = len(parts[1])
                        str_data = str(new_data)
                        if decimal_length < self.map_precision:
                            for x in range(self.map_precision - decimal_length):
                                str_data += "0"
                        map_decimal = True
                    else:
                        data[index] = int(round(data[index]))
                        map_decimal = False
                    self.ui.map_decimal = map_decimal
                    if not map_decimal:
                        self.ui.box_layout.setItem(i, j, QTableWidgetItem(f"{int(data[index]):05}"))
                        if not new:
                            self.ui.original[i][j] = data[index]
                    else:
                        parts = str_data.split('.')
                        self.ui.box_layout.setItem(i, j, QTableWidgetItem(f"{int(parts[0]):05}.{parts[1]}"))
                        self.ui.new_width = len(self.ui.box_layout.item(i, j).text()) - 1
                        if not new:
                            self.ui.original[i][j] = float(self.ui.box_layout.item(i, j).text().strip())
                    index += 1
                    self.ui.box_layout.item(i, j).setForeground(QColor("white"))

            self.adjust_row_width(x_precision)
        else:
            clipboard = QApplication.clipboard()
            clipboard_text = clipboard.text()  # get text from clipboard

            if clipboard_text[-1] == '\n':
                clipboard_text = clipboard_text[:-1]

            values_clipboard = re.split(r'[\t\n]', clipboard_text)

            length_of_original = (sum(len(sublist) for sublist in self.ui.original))

            if len(values_clipboard) != length_of_original:
                QMessageBox.warning(self.ui, "Warning", "Data size is not right!")
                return

            for i in range(len(values_clipboard)):
                try:
                    int(values_clipboard[i])
                except ValueError:
                    QMessageBox.warning(self.ui, "Warning", "Data is not correct!")
                    return

            x = 0
            row_start = 0
            col_start = 0

            for i in range(len(clipboard_text)):
                if x >= len(values_clipboard):
                    break

                if clipboard_text[i] == '\t':
                    item = self.ui.box_layout.item(row_start, col_start)
                    if item:
                        int_val = int(values_clipboard[x])
                        item.setText(f"{int_val:05}")
                    x += 1

                    if col_start + 1 >= self.ui.columns:
                        row_start += 1
                        col_start = 0
                    else:
                        col_start += 1

                elif clipboard_text[i] == '\n':
                    item = self.ui.box_layout.item(row_start, col_start)
                    if item:
                        int_val = int(values_clipboard[x])
                        item.setText(f"{int_val:05}")
                    x += 1

                    row_start += 1
                    col_start = 0

            item = self.ui.box_layout.item(row_start, col_start)
            if item:
                int_val = int(values_clipboard[x])
                item.setText(f"{int_val:05}")

    def paste_x_data(self, maps, data, new):
        if maps:
            maps = self.ui.maps
            with open(maps.file_path, 'r') as file:
                content = file.read().split('\n')
            index = maps.last_map_index
            index *= 10

            try:
                x_factor = float(content[index + 6])
                x_precision = int(content[index + 7])
            except ValueError:
                QMessageBox.warning(self.ui, "Warning",
                                    "There is a problem with the mappack file. It appears to have been modified by an user."
                                    "\nPlease restart the application!")
                return

            str_data = ""

            self.ui.x_values = []

            for i in range(len(data)):
                data = list(data)
                data[i] = int(data[i])

                if x_factor != 1.0:
                    data[i] *= x_factor
                self.ui.x_values.append(data[i])
                if x_precision != 0:
                    new_data = float(round(data[i], x_precision))
                    parts = str(new_data).split('.')
                    decimal_length = len(parts[1])
                    str_data = str(new_data)
                    if decimal_length < x_precision:
                        for x in range(x_precision - decimal_length):
                            str_data += "0"
                    x_decimal = True
                else:
                    data[i] = int(round(data[i]))
                    x_decimal = False

                self.ui.x_axis_decimal = x_decimal

                if not x_decimal:
                    self.ui.box_layout.horizontalHeaderItem(i).setText(f"{int(data[i]):05}")
                    if not new:
                        self.ui.original_x[i] = data[i]
                else:
                    parts = str_data.split('.')
                    self.ui.box_layout.horizontalHeaderItem(i).setText(f"{int(parts[0]):05}.{parts[1]}")

                    if not new:
                        self.ui.original_x[i] = float(self.ui.box_layout.horizontalHeaderItem(i).text().strip())

            self.adjust_row_width(x_precision)
        else:
            clipboard = QApplication.clipboard()
            clipboard_text = clipboard.text()  # get text from clipboard

            if clipboard_text[-1] == '\n':
                clipboard_text = clipboard_text[:-1]

            values_clipboard = clipboard_text.split('\t')

            if len(values_clipboard) != self.ui.num_columns_3d:
                QMessageBox.warning(self.ui, "Warning", "Data size is not right!")
                return

            for i in range(len(values_clipboard)):
                try:
                    int(values_clipboard[i])
                except ValueError:
                    QMessageBox.warning(self.ui, "Warning", "Data is not correct!")
                    return

            for i in range(len(values_clipboard)):
                item = self.ui.box_layout.horizontalHeaderItem(i)
                int_val = int(values_clipboard[i])
                item.setText(f"{int_val:05}")
                self.check_difference_x(i)

    def paste_y_data(self, maps, data, new):
        if maps:
            maps = self.ui.maps
            with open(maps.file_path, 'r') as file:
                content = file.read().split('\n')
            index = maps.last_map_index
            index *= 10

            try:
                y_factor = float(content[index + 8])
                y_precision = int(content[index + 9])
            except ValueError:
                QMessageBox.warning(self.ui, "Warning",
                                    "There is a problem with the mappack file. It appears to have been modified by an user."
                                    "\nPlease restart the application!")
                return

            str_data = ""

            self.ui.y_values = []

            for i in range(len(data)):
                data = list(data)
                data[i] = int(data[i])

                if y_factor != 1.0:
                    data[i] *= y_factor
                self.ui.y_values.append(data[i])
                if y_precision != 0.0:
                    new_data = float(round(data[i], y_precision))
                    parts = str(new_data).split('.')
                    decimal_length = len(parts[1])
                    str_data = str(new_data)
                    if decimal_length < y_precision:
                        for x in range(y_precision - decimal_length):
                            str_data += "0"
                    y_decimal = True
                else:
                    data[i] = int(round(data[i]))
                    y_decimal = False
                self.ui.y_axis_decimal = y_decimal
                if not y_decimal:
                    self.ui.box_layout.verticalHeaderItem(i).setText(f"{int(data[i]):05}")
                    if not new:
                        self.ui.original_y[i] = data[i]
                else:
                    parts = str_data.split('.')
                    self.ui.box_layout.verticalHeaderItem(i).setText(f"{int(parts[0]):05}.{parts[1]}")

                if not new:
                    self.ui.original_y[i] = float(self.ui.box_layout.verticalHeaderItem(i).text().strip())

            add_width_y = 0
            if self.ui.y_axis_decimal:
                for y in range(y_precision):
                    if y > 0:
                        add_width_y += 10
                    else:
                        add_width_y += 12
            self.ui.box_layout.verticalHeader().setFixedWidth(55 + add_width_y)
        else:
            clipboard = QApplication.clipboard()
            clipboard_text = clipboard.text()  # get text from clipboard

            if clipboard_text[-1] == '\n':
                clipboard_text = clipboard_text[:-1]

            values_clipboard = clipboard_text.split('\n')

            if len(values_clipboard) != self.ui.num_rows_3d:
                QMessageBox.warning(self.ui, "Warning", "Data size is not right!")
                return

            for i in range(len(values_clipboard)):
                try:
                    int(values_clipboard[i])
                except ValueError:
                    QMessageBox.warning(self.ui, "Warning", "Data is not correct!")
                    return

            for i in range(len(values_clipboard)):
                item = self.ui.box_layout.verticalHeaderItem(i)
                int_val = int(values_clipboard[i])
                item.setText(f"{int_val:05}")
                self.check_difference_y(i)

    def adjust_row_width(self, x_precision):
        add_width_map = 0
        if self.ui.map_decimal:
            for i in range(self.map_precision):
                if i > 0:
                    add_width_map += 10
                else:
                    add_width_map += 12

        add_width_x = 0
        if self.ui.x_axis_decimal:
            for i in range(x_precision):
                if i > 0:
                    add_width_x += 10
                else:
                    add_width_x += 12

        if add_width_x > add_width_map:
            add_width = add_width_x
        elif add_width_x < add_width_map:
            add_width = add_width_map
        else:
            add_width = add_width_map

        for col in range(self.ui.num_columns_3d):  # change column width
            self.ui.box_layout.setColumnWidth(col, self.ui.column_width_3d + add_width)

    def check_difference(self, row, col):
        entry = self.ui.box_layout.item(row, col)
        original_value = float(self.ui.original[row][col])

        if len(entry.text()) > 5 and not self.ui.map_decimal:
            current_text = entry.text()

            int_part, decimal_part = current_text.split('.')

            cut_counter = len(decimal_part) + 1

            entry.setText(current_text[:cut_counter * -1])

        try:
            current_value = float(entry.text())
            if current_value > 65535 or current_value < 0:
                raise ValueError
        except ValueError:
            current_text = entry.text()
            int_part, decimal_part = current_text.split('.')

            cut_counter = len(decimal_part) + 1

            entry.setText(current_text[:cut_counter * -1])
            return

        if current_value > original_value:
            entry.setForeground(QColor("red"))
        elif current_value < original_value:
            entry.setForeground(QColor("blue"))
        else:
            entry.setForeground(QColor("white"))

        self.on_selection_3d()

    def check_difference_x(self, j):
        entry = self.ui.box_layout.horizontalHeaderItem(j)
        original_value = float(self.ui.original_x[j])

        if len(entry.text()) > 5 and not self.ui.x_axis_decimal:
            current_text = entry.text()
            entry.setText(current_text[:-1])

        try:
            current_value = float(entry.text())
            if current_value > 65535 or current_value < 0:
                raise ValueError
        except ValueError:
            current_text = entry.text()
            entry.setText(current_text[:-1])
            return

        if current_value > original_value:
            entry.setForeground(QColor("red"))
        elif current_value < original_value:
            entry.setForeground(QColor("blue"))
        else:
            entry.setForeground(QColor("white"))

    def check_difference_y(self, i):
        entry = self.ui.box_layout.verticalHeaderItem(i)
        original_value = float(self.ui.original_y[i])

        if len(entry.text()) > 5 and not self.ui.y_axis_decimal:
            current_text = entry.text()
            entry.setText(current_text[:-1])

        try:
            current_value = float(entry.text())
            if current_value > 65535 or current_value < 0:
                raise ValueError
        except ValueError:
            current_text = entry.text()
            entry.setText(current_text[:-1])
            return

        if current_value > original_value:
            entry.setForeground(QColor("red"))
        elif current_value < original_value:
            entry.setForeground(QColor("blue"))
        else:
            entry.setForeground(QColor("white"))

    def paste_map(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()

        striped_text = [list(re.split(r'[\t]+', line)) for line in clipboard_text.strip().split('\n')]

        x_axis_data = striped_text[0]

        x_axis_text = '\t'.join([text for text in x_axis_data])

        clipboard.setText(x_axis_text)

        self.paste_x_data(False, [], False)

        y_axis_text = '\n'.join([striped_text[i][0] for i in range(1, len(striped_text) - 1)] + [striped_text[-1][0]])

        clipboard.setText(y_axis_text)

        self.paste_y_data(False, [], False)

        map_values = ""
        for i in range(1, len(striped_text)):
            row_text = '\t'.join(striped_text[i][1:])
            map_values += row_text + '\n'

        clipboard.setText(map_values)

        self.paste_data(False, [], 0, 0, False, "")

        clipboard.setText(clipboard_text)

    def copy_map(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()

        x_axis_values = self.copy_x_axis()
        y_axis_values = self.copy_y_axis()

        map_values = "\t" + "\t".join(x_axis_values) + "\n"

        for i in range(self.ui.box_layout.rowCount()):
            row_values = [y_axis_values[i]]
            for j in range(self.ui.box_layout.columnCount()):
                entry = self.ui.box_layout.item(i, j)
                if entry is not None:
                    row_values.append(entry.text())
                else:
                    row_values.append("")

            map_values += "\t".join(row_values) + "\n"

        clipboard.setText(map_values.strip('\n'))

    def copy_x_axis(self):
        values_data = []
        for col in range(self.ui.num_columns_3d):
            value = self.ui.box_layout.horizontalHeaderItem(col).text()
            values_data.append(value)

        return values_data


    def copy_y_axis(self):
        values_data = []
        for row in range(self.ui.num_rows_3d):
            value = self.ui.box_layout.verticalHeaderItem(row).text()
            values_data.append(value)

        return values_data

    def check_all(self):
        rows = self.ui.num_rows_3d
        cols = self.ui.num_columns_3d

        for row in range(rows):
            for col in range(cols):
                self.check_difference(row, col)

            self.check_difference_y(row)

        for col in range(cols):
            self.check_difference_x(col)

    def validate_cell_input(self, item: QTableWidgetItem):
        self.ui.box_layout.blockSignals(True) # block all signals

        row = item.row()
        col = item.column()
        value = item.text()

        try:
            float_value = float(value)
            if float_value < 0 or float_value > 65535:
                raise ValueError

            if '.' in value:
                int_part, dec_part = value.split('.')

                formatted_int = int_part.zfill(5)

                formatted_number = f"{formatted_int}.{dec_part}"
                item.setText(formatted_number)
            else:
                if self.ui.map_decimal:
                    map_name = self.ui.map_list.item(self.ui.maps.last_map_index).text()
                    with open(self.ui.maps.file_path, 'r') as file:
                        content = file.read().split('\n')
                        for i in range(len(content)):
                            if content[i] == map_name:
                                try:
                                    precision = int(content[i + 5])
                                except ValueError:
                                    QMessageBox.warning(self.ui, "Warning",
                                                        "There is a problem with the mappack file. It appears to have been modified by an user."
                                                        "\nPlease restart the application!")
                                    return

                    new_value = f"{int(float_value):05}.{'0' * precision}"
                    item.setText(new_value)
                else:
                    new_value = f"{int(float_value):05}"
                    item.setText(new_value)

        except ValueError:
            value_ori = float(self.ui.original[row][col])
            if '.' in value:
                integer_part, decimal_part = str(value_ori).split('.')

                formatted_integer = integer_part.zfill(5)

                formatted_number = f"{formatted_integer}.{decimal_part}"
                item.setText(formatted_number)
            else:
                if self.ui.map_decimal:
                    map_name = self.ui.map_list.item(self.ui.maps.last_map_index).text()
                    with open(self.ui.maps.file_path, 'r') as file:
                        content = file.read().split('\n')
                        for i in range(len(content)):
                            if content[i] == map_name:
                                try:
                                    precision = int(content[i + 5])
                                except ValueError:
                                    QMessageBox.warning(self.ui, "Warning",
                                                        "There is a problem with the mappack file. It appears to have been modified by an user."
                                                        "\nPlease restart the application!")
                                    return
                    item.setText(f"{value_ori:05}.{'0' * precision}")
                else:
                    item.setText(f"{int(value_ori):05}")

        self.check_difference(row, col)

        self.ui.tk_win_manager.call_update_3d()

        self.ui.box_layout.blockSignals(False)  # unblock all signals

    def set_default(self): # sets 3d tab at default values
        self.resize_grid(10, 10, False)

        self.ui.box_layout.setUpdatesEnabled(False)  # Stop redrawing during fill
        for row in range(self.ui.box_layout.rowCount()): # insert 0
            for col in range(self.ui.box_layout.columnCount()):
                self.ui.box_layout.setItem(row, col, QTableWidgetItem(f"{0:05}"))
        self.ui.box_layout.setUpdatesEnabled(True)  # Re-enable drawing

        # insert both axis
        horizontal_headers = [f"{i + 1:05}" for i in range(self.ui.num_columns_3d)]
        vertical_headers = [f"{i + 1:05}" for i in range(self.ui.num_rows_3d)]

        self.ui.box_layout.setHorizontalHeaderLabels(horizontal_headers)
        self.ui.box_layout.setVerticalHeaderLabels(vertical_headers)

        for col in range(self.ui.num_columns_3d):
            header_item = QTableWidgetItem(horizontal_headers[col])
            self.ui.box_layout.setHorizontalHeaderItem(col, header_item)

        for row in range(self.ui.num_rows_3d):
            header_item = QTableWidgetItem(vertical_headers[row])
            self.ui.box_layout.setVerticalHeaderItem(row, header_item)

        for col in range(self.ui.num_columns_3d): # change column width
            self.ui.box_layout.setColumnWidth(col, self.ui.column_width_3d)

        self.ui.map_opened = False

    def paste_selected(self):
        selected_items = self.ui.box_layout.selectedItems()

        if not selected_items:
            QMessageBox.warning(self.ui, "Warning", "No item selected!")
            return

        first_item = selected_items[0]  # first selected item
        row_ori = first_item.row()  # current row
        col_ori = first_item.column()  # current column

        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()  # get text from clipboard

        if clipboard_text[-1] == '\n':
            clipboard_text = clipboard_text[:-1]

        values_clipboard = re.split(r'[\t\n]', clipboard_text)

        index = (row_ori * self.ui.num_columns_3d) + col_ori

        length_of_original = (sum(len(sublist) for sublist in self.ui.original))

        end_length = len(values_clipboard) + index

        if length_of_original < end_length:
            QMessageBox.warning(self.ui, "Warning", "Data size is not right!")
            return

        for i in range(len(values_clipboard)):
            try:
                int(values_clipboard[i])
            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Data is not correct!")
                return

        x = 0
        row_start = row_ori
        col_start = col_ori

        for i in range(len(clipboard_text)):
            if x >= len(values_clipboard):
                break

            if clipboard_text[i] == '\t':
                item = self.ui.box_layout.item(row_start, col_start)
                if item:
                    int_val = int(values_clipboard[x])
                    item.setText(f"{int_val:05}")
                x += 1

                if col_start + 1 >= self.ui.columns:
                    row_start += 1
                    col_start = 0
                else:
                    col_start += 1

            elif clipboard_text[i] == '\n':
                item = self.ui.box_layout.item(row_start, col_start)
                if item:
                    int_val = int(values_clipboard[x])
                    item.setText(f"{int_val:05}")
                x += 1

                row_start += 1
                col_start = col_ori

        item = self.ui.box_layout.item(row_start, col_start)
        if item:
            int_val = int(values_clipboard[x])
            item.setText(f"{int_val:05}")

    def on_selection_3d(self):
        selected_items = self.ui.box_layout.selectedItems()

        if len(selected_items) == 1:
            selected_index = selected_items[0]
            row = selected_index.row()
            col = selected_index.column()

            item_text = self.ui.box_layout.item(row, col).text()

            ori_val = self.ui.original[row][col]

            if not self.ui.map_decimal:
                if len(item_text) > 5:
                    diff_value = round(int(float(item_text) - float()), 0)
                else:
                    diff_value = round(int(item_text) - int(ori_val), 0)
            else:
                if len(item_text.split('.')) > 1:
                    parts_text = item_text.split('.')

                    float_len = len(parts_text[1])
                else:
                    float_len = 0
                diff_value = round(float(item_text) - float(ori_val), float_len)

            if diff_value != 0:
                if not self.ui.map_decimal:
                    self.ui.diff_btn_3d.setText(f"Diff: {diff_value:05}")
                else:
                    parts = str(diff_value).split('.')
                    self.ui.diff_btn_3d.setText(f"Diff: {int(parts[0]):05}.{parts[1]}")
                current_val = float(item_text)
                if current_val != 0 and ori_val != 0:
                    percentage_change = min(((current_val / ori_val) - 1) * 100, 999.99)
                    self.ui.diff_btn_per_3d.setText(f"Diff: {percentage_change:.2f}%")
                else:
                    if current_val == ori_val:
                        self.ui.diff_btn_per_3d.setText(f"Diff: 0.00%")
                    else:
                        self.ui.diff_btn_per_3d.setText(f"Diff: 100.00%")
            else:
                self.ui.diff_btn_3d.setText("Diff: 00000")
                self.ui.diff_btn_per_3d.setText(f"Diff: 0.00%")

            self.ui.ori_val_btn_3d.setText(f"Ori: {int(ori_val):05}")
        else:
            self.ui.diff_btn_3d.setText("Diff: 00000")
            self.ui.ori_val_btn_3d.setText(f"Ori: 00000")
            self.ui.diff_btn_per_3d.setText(f"Diff: 0.00%")

    def edit_horizontal_header(self, index):
        current_text = self.ui.box_layout.horizontalHeaderItem(index).text()
        value, ok = QInputDialog.getText(self.ui, "Edit X-Axis", "Enter a new value:", text=current_text)
        try:
            float_value = float(value)
            if float_value < 0 or float_value > 65535:
                raise ValueError

            if '.' in value:
                int_part, dec_part = value.split('.')

                formatted_int = int_part.zfill(5)

                value = f"{formatted_int}.{dec_part}"
            else:
                if self.ui.x_axis_decimal:
                    map_name = self.ui.map_list.item(self.ui.maps.last_map_index).text()
                    with open(self.ui.maps.file_path, 'r') as file:
                        content = file.read().split('\n')
                        for i in range(len(content)):
                            if content[i] == map_name:
                                try:
                                    precision = int(content[i + 7])
                                except ValueError:
                                    QMessageBox.warning(self.ui, "Warning",
                                                        "There is a problem with the mappack file. It appears to have been modified by an user."
                                                        "\nPlease restart the application!")
                                    return
                    value = f"{int(float_value):05}.{'0' * precision}"
                else:
                    value = f"{int(float_value):05}"

        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Enter a valid value!")
            return
        if ok and value:
            self.ui.box_layout.horizontalHeaderItem(index).setText(value)
            self.check_difference_x(index)

    def edit_vertical_header(self, index):
        current_text = self.ui.box_layout.verticalHeaderItem(index).text()
        value, ok = QInputDialog.getText(self.ui, "Edit Y-Axis", "Enter a new value:", text=current_text)
        try:
            float_value = float(value)
            if float_value < 0 or float_value > 65535:
                raise ValueError

            if '.' in value:
                int_part, dec_part = value.split('.')

                formatted_int = int_part.zfill(5)

                value = f"{formatted_int}.{dec_part}"
            else:
                if self.ui.x_axis_decimal:
                    map_name = self.ui.map_list.item(self.ui.maps.last_map_index).text()
                    with open(self.ui.maps.file_path, 'r') as file:
                        content = file.read().split('\n')
                        for i in range(len(content)):
                            if content[i] == map_name:
                                try:
                                    precision = int(content[i + 9])
                                except ValueError:
                                    QMessageBox.warning(self.ui, "Warning",
                                                        "There is a problem with the mappack file. It appears to have been modified by an user."
                                                        "\nPlease restart the application!")
                                    return
                    value = f"{int(float_value):05}.{'0' * precision}"
                else:
                    value = f"{int(float_value):05}"

        except ValueError:
            QMessageBox.warning(self.ui, "Warning", "Enter a valid value!")
            return
        if ok and value:
            self.ui.box_layout.verticalHeaderItem(index).setText(value)
            self.check_difference_y(index)

    def set_ori_value(self, row, col):
        self.ui.box_layout.item(row, col).setText(str(int(self.ui.original[row][col])))
