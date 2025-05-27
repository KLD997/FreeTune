import os
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QItemSelectionModel, QTimer


class Maps_Utility:
    def __init__(self, ui):
        self.ui = ui
        self.file_path = "mappack.mp"
        self.map_data = []
        self.x_axis = []
        self.y_axis = []
        self.map_name = ""
        self.size = ""
        self.start_index = 0
        self.end_index = 0
        self.first_run = True
        self.row = 0
        self.col = 0
        self.last_map_index = 0
        self.double_click = False

    def add_map(self):
        from text_addons import TextAddons
        text_addons_ = TextAddons(self.ui)
        if not text_addons_.copy_values(True):
            return

        selection_model = self.ui.table_view.selectionModel()  # get all selected items
        selected_indexes = selection_model.selectedIndexes()  # all selected items

        first_row = selected_indexes[0].row()
        first_col = selected_indexes[0].column()

        last_row = selected_indexes[-1].row()
        last_col = selected_indexes[-1].column()

        self.start_index = (first_row * self.ui.columns) + first_col - self.ui.shift_count
        self.end_index = (last_row * self.ui.columns) + last_col - self.ui.shift_count

        clipboard = QApplication.clipboard() # get data from clipboard
        clipboard_text = clipboard.text() # get text from clipboard

        map_data = clipboard_text.strip().split()
        self.find_factors((len(map_data)))

    def find_factors(self, data):
        factors = []
        for i in range(41):
            x = i + 1
            if data % x == 0:
                factors.append(x)  # columns
                factors.append(data / x)  # rows
        if factors:
            self.factor_dialog(factors)

    def factor_dialog(self, factors):
        from custom_dialogs.maps_dialogs import Factor_Dialog
        dialog = Factor_Dialog(self.ui, self, factors)
        dialog.exec()

    def map_name_dialog(self):
        from custom_dialogs.maps_dialogs import Map_Name_Dialog
        dialog = Map_Name_Dialog(self.ui, self)
        dialog.exec()

    def value_changer_dialog(self):
        from custom_dialogs.value_dialog_3d import ValueDialog3D
        dialog = ValueDialog3D(self.ui)
        dialog.exec()

    def map_properties_dialog(self, option):
        if not self.ui.map_opened:
            QMessageBox.warning(self.ui, "Warning", "Please open a map!")
            return
        if option == "map":
            from custom_dialogs.map_properties_window import MapProperties
            dialog = MapProperties(self.ui)
        elif option == "x":
            from custom_dialogs.x_axis_properties_window import XAxisProperties
            dialog = XAxisProperties(self.ui)
        else:
            from custom_dialogs.y_axis_properties_window import YAxisProperties
            dialog = YAxisProperties(self.ui)

        dialog.exec()


    def create_map(self, map_name):
        if map_name == "":
            return
        self.map_name = map_name
        if not self.first_run:
            with open(self.file_path, 'r') as file:
                content = file.read().split('\n')
                for i in range(len(content)):
                    if content[i] == self.map_name:
                        QMessageBox.warning(self.ui, "Warning", "This name is already in use! Choose a new one!")
                        if self.ui.potential_map_added:
                            self.ui.potential_map_added = False
                        return

        self.first_run = False
        self.ui.map_list.insertItem(self.ui.map_list_counter, self.map_name)
        self.ui.maps_names.append(self.map_name)
        self.highlight_2d_map(self.start_index, self.end_index)
        self.write_file_mp()
        self.ui.map_list_counter += 1

        if self.ui.potential_map_added:
            self.ui.potential_maps_start.pop(self.ui.potential_map_index)
            self.ui.potential_maps_end.pop(self.ui.potential_map_index)

    def write_file_mp(self):
        with open(self.file_path, 'a') as file:
            file.write(f"\n{self.map_name}\n" if self.ui.map_list_counter > 0 else f"{self.map_name}\n")
            file.write(f"{self.start_index}\n")
            file.write(f"{self.end_index}\n")
            file.write(f"{self.size}\n")
            file.write(f"{1.0}\n") # map factor
            file.write(f"{0}\n") # map decimals
            file.write(f"{1.0}\n") # x-axis factor
            file.write(f"{0}\n") # x-axis decimals
            file.write(f"{1.0}\n") # y-axis factor
            file.write(f"{0}") # y-axis decimals

    def auto_enable_context_menu(self):
        self.ui.box_layout.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)

    def open_map_right_click(self):
        self.ui.box_layout.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.timer = QTimer(self.ui)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.auto_enable_context_menu)
        self.timer.start()

        selection_model = self.ui.table_view.selectionModel()
        selection_indexes = selection_model.selectedIndexes()

        if len(selection_indexes) == 1:
            row = selection_indexes[0].row()
            col = selection_indexes[0].column()

            index = self.ui.model.index(row, col)

            bg_color = self.ui.model.data(index, Qt.ItemDataRole.BackgroundRole)

            index_value = (row * self.ui.columns) + col

            if bg_color is not None:
                if bg_color.name() == "#85d7f2":
                    try:
                        with open(self.file_path, 'r') as file:
                            content = file.read().split('\n')
                            for i in range(len(content)):
                                if "x" in content[i]:
                                    start = int(content[i - 2]) + self.ui.shift_count
                                    end = int(content[i - 1]) + self.ui.shift_count

                                    if start <= index_value <= end:
                                        if i - 3 != 0:
                                            map_index = (i - 3 + 1) // 10
                                        else:
                                            map_index = 0
                                        self.last_map_index = map_index
                                        self.double_click = True
                                        self.ui.tabs.setCurrentIndex(2)
                                        self.update_3d_from_text()
                                        break
                    except ValueError:
                        QMessageBox.warning(self.ui, "Warning",
                                            "There is a problem with the mappack file. It appears to have been modified by an user."
                                            "\nPlease restart the application!")
                        return

    def on_double_click(self, item):
        index = self.ui.map_list.row(item)
        self.double_click = True
        self.last_map_index = index
        self.update_3d_from_text()
        self.ui.tabs.setCurrentIndex(2)

    def update_3d_from_text(self):
        if not os.path.exists(self.file_path) or self.ui.map_list_counter == 0:
            return

        item = self.ui.map_list.item(self.last_map_index).text()

        with open(self.file_path, 'r') as file:
            content = file.readlines()
            item_index = -1

            for i, line in enumerate(content):
                if line.strip() == item:
                    item_index = i
                    break

            if item_index == -1:
                return

            try:
                start_index_unpacked = int(content[item_index + 1])
                end_index_unpacked = int(content[item_index + 2]) + 1

                start_index_current = start_index_unpacked + self.ui.shift_count
                end_index_current = end_index_unpacked + self.ui.shift_count
                size = content[item_index + 3].strip()
            except ValueError:
                QMessageBox.warning(self.ui, "Warning",
                                    "There is a problem with the mappack file. It appears to have been modified by an user."
                                    "\nPlease restart the application!")
                return

            self.col, self.row = map(int, size.split('x'))

            self.map_data = self.ui.unpacked[start_index_unpacked:end_index_unpacked]
            self.ui.mode3d.paste_data(True, self.map_data, self.row, self.col, False, item)

            if start_index_unpacked >= self.col + self.row:
                self.x_axis = self.ui.unpacked[start_index_unpacked - self.col:start_index_unpacked]
                self.y_axis = self.ui.unpacked[start_index_unpacked - (self.col + self.row):start_index_unpacked - self.col]
                self.ui.mode3d.paste_x_data(True, self.x_axis, False)
                self.ui.mode3d.paste_y_data(True, self.y_axis, False)

            values = self.ui.model.get_all_data()

            self.ui.current_values = []

            for i in range(self.ui.shift_count):
                self.ui.current_values.append(None)

            for row in values:
                for col in row:
                    if col is not None:
                        self.ui.current_values.append(col)

            self.map_data = self.ui.current_values[start_index_current:end_index_current]
            self.ui.mode3d.paste_data(True, self.map_data, self.row, self.col, True, item)

            if start_index_current >= self.col + self.row:
                self.x_axis = self.ui.current_values[start_index_current - self.col:start_index_current]
                self.y_axis = self.ui.current_values[start_index_current - (self.col + self.row):start_index_current - self.col]
                self.ui.mode3d.paste_x_data(True, self.x_axis, True)
                self.ui.mode3d.paste_y_data(True, self.y_axis, True)

        self.ui.mode3d.check_all()

        self.ui.map_opened = True

    def highlight_2d_map(self, start_index, end_index):
        self.ui.start_index_maps.append(start_index)
        self.ui.end_index_maps.append(end_index)

        self.ui.sync_2d_scroll = True
        self.ui.mode2d.draw_canvas(self.ui)

    def write_map(self):
        if not os.path.exists(self.file_path) or self.ui.map_list_counter == 0:
            return

        map_values = []
        item = self.ui.map_list.item(self.last_map_index).text()

        if not self.double_click:
            return

        with open(self.file_path, 'r') as file:
            content = file.read().split('\n')
            for i in range(len(content)):
                if content[i] == item:
                    try:
                        map_factor = float(content[i + 4])
                        x_axis_factor = float(content[i + 6])
                        y_axis_factor = float(content[i + 8])
                    except ValueError:
                        QMessageBox.warning(self.ui, "Warning",
                                            "There is a problem with the mappack file. It appears to have been modified by an user."
                                            "\nPlease restart the application!")
                        return

        values = self.ui.model.get_all_data() # get current values

        self.ui.current_values = []

        for i in range(self.ui.shift_count):
            self.ui.current_values.append(None)

        for row in values:
            for col in row:
                if col is not None:
                    self.ui.current_values.append(col)

        for i in range(self.ui.num_rows_3d): # get y axis values
            value_entry = float(self.ui.box_layout.verticalHeaderItem(i).text())
            value_before = round(self.ui.y_values[i])
            if (value_entry - value_before) != 0:
                value = value_entry
            else:
                value = self.ui.y_values[i]
            value /= y_axis_factor
            value = round(value)
            map_values.append(int(value))

        for i in range(self.ui.num_columns_3d): # get x axis values
            value_entry = float(self.ui.box_layout.horizontalHeaderItem(i).text())
            value_before = round(self.ui.x_values[i])
            if (value_entry - value_before) != 0:
                value = value_entry
            else:
                value = self.ui.x_values[i]
            value /= x_axis_factor
            value = round(value)
            map_values.append(int(value))

        index_map = 0
        for i in range(self.ui.num_rows_3d): # get map values
            for x in range(self.ui.num_columns_3d):
                value_entry = float(self.ui.box_layout.item(i, x).text())
                value_before = round(self.ui.map_values[index_map])
                if (value_entry - value_before) != 0:
                    value = value_entry
                else:
                    value = self.ui.map_values[index_map]
                value /= map_factor
                value = round(value)
                map_values.append(int(value))
                index_map += 1

        with open(self.file_path, 'r') as file:
            content = file.read().split('\n')
            index = self.last_map_index * 10
            try:
                start = int(content[index + 1]) + self.ui.shift_count
                end = int(content[index + 2]) + self.ui.shift_count
            except ValueError:
                QMessageBox.warning(self.ui, "Warning",
                                    "There is a problem with the mappack file. It appears to have been modified by an user."
                                    "\nPlease restart the application!")
                return

        x = 0

        for i in range(start - (self.ui.num_rows_3d + self.ui.num_columns_3d), end + 1):
            self.ui.current_values[i] = map_values[x]
            x += 1

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

        self.ui.mode2d.draw_canvas(self.ui)

    def remove_item(self):
        selected_index = self.ui.map_list.currentRow()
        item = self.ui.map_list.item(selected_index).text()

        reply = QMessageBox.question(
            self.ui,
            'Confirm Action',
            f"Are you sure you want to remove the map: {item}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        start_index = 0
        end_index = 0

        if self.last_map_index == selected_index:
            self.ui.mode3d.set_default()
        with open(self.file_path, 'r') as file:
            content = file.read().split("\n")
            for i in range(len(content)):
                if content[i] == item:
                    try:
                        start_index = int(content[i + 1])
                        end_index = int(content[i + 2])
                    except ValueError:
                        QMessageBox.warning(self.ui, "Warning",
                                            "There is a problem with the mappack file. It appears to have been modified by an user."
                                            "\nPlease restart the application!")
                        return
                    del content[i:i + 10]
                    break
        with open(self.file_path, 'w') as file:
            for i in range(len(content)):
                file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])
        self.ui.map_list_counter -= 1
        self.ui.map_list.takeItem(selected_index)

        self.ui.start_index_maps.remove(start_index)
        self.ui.end_index_maps.remove(end_index)

        self.ui.mode2d.draw_canvas(self.ui)

    def show_map_in_text(self):
        selected_index = self.ui.map_list.currentRow()
        item = self.ui.map_list.item(selected_index).text()

        if self.last_map_index == selected_index:
            self.ui.mode3d.set_default()
        with open(self.file_path, 'r') as file:
            content = file.read().split("\n")
            for i in range(len(content)):
                if content[i] == item:
                    try:
                        start_index = int(content[i + 1])
                    except ValueError:
                        QMessageBox.warning(self.ui, "Warning",
                                            "There is a problem with the mappack file. It appears to have been modified by an user."
                                            "\nPlease restart the application!")
                        return
                    del content[i:i + 10]
                    break

        self.ui.mode2d.highlight_text(start_index, True)
        self.ui.mode2d.text_to_2d(self.ui)

        self.ui.tabs.setCurrentIndex(0)

    def import_map(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        file_path, selected_filter = QFileDialog.getOpenFileName(self.ui, "Import MapPack", "", "MapPack Files (*.mp)")

        if file_path:
            try:
                self.ui.map_list_counter = 0
                self.last_map_index = 0
                mode3d = self.ui.mode3d
                mode3d.set_default()
                with open(file_path, 'r') as file:
                    content = file.read().split('\n')
                    if len(content) % 10 == 0:
                        with open(self.file_path, 'w') as temp_file:
                            for i in range(len(content)):
                                temp_file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])
                            self.ui.map_list.clear()
                            self.ui.start_index_maps.clear()
                            self.ui.end_index_maps.clear()
                            self.ui.maps_names = []
                            self.first_run = False
                        for i in range(len(content) // 10):
                            self.map_name = content[i * 10]
                            self.start_index = int(content[(i * 10) + 1])
                            self.end_index = int(content[(i * 10) + 2])
                            self.size = content[(i * 10) + 3]
                            self.ui.map_list.insertItem(self.ui.map_list_counter, self.map_name)
                            self.ui.maps_names.append(self.map_name)
                            self.highlight_2d_map(self.start_index, self.end_index)
                            self.ui.map_list_counter += 1
                    else:
                        raise ValueError
            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Please select a valid file!")
                self.ui.map_list_counter -= 1
                self.ui.map_list.clear()

                self.ui.start_index_maps.clear()
                self.ui.end_index_maps.clear()

    def export_map(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        if not self.ui.map_list_counter:
            QMessageBox.warning(self.ui, "Warning", "You have to create or import a mappack before you can export it!")
            return

        file_path, selected_filter = QFileDialog.getSaveFileName(self.ui, "Save File", "MapPack.mp", "MapPack Files (*.mp)")

        if file_path:
            with open(self.file_path, 'r') as ori:
                content = ori.read().split('\n')

            with open(file_path, 'w') as file:
                for i in range(len(content)):
                    file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])

        else:
            QMessageBox.warning(self.ui, "Warning", "No file was selected for saving!")

    def sign_values(self):
        if self.ui.signed_values:
            self.ui.signed_values = False
        else:
            self.ui.signed_values = True

    def add_potential_map(self):
        selection_model = self.ui.table_view.selectionModel()
        selection_indexes = selection_model.selectedIndexes()

        if len(selection_indexes) == 1:
            row = selection_indexes[0].row()
            col = selection_indexes[0].column()

            index_value = (row * self.ui.columns) + col

            self.ui.potential_map_index = None

            selected_indexes = []
            for i in range(len(self.ui.potential_maps_start)):
                start = self.ui.potential_maps_start[i]
                end = self.ui.potential_maps_end[i]

                if start <= index_value <= end:
                    for j in range(start, end + 1):
                        selected_row = j // self.ui.columns
                        selected_col = j % self.ui.columns
                        selected_indexes.append(self.ui.table_view.model().index(selected_row, selected_col))
                    self.ui.potential_map_index = i
                    break

            if self.ui.potential_map_index is None:
                QMessageBox.warning(self.ui, "Warning", "There is no potential map on the selected cell!")
                return

            if selected_indexes:
                for index in selected_indexes:
                    selection_model.select(index, QItemSelectionModel.SelectionFlag.Select)

                self.add_map()

    def remove_potential_map(self):
        selection_model = self.ui.table_view.selectionModel()
        selection_indexes = selection_model.selectedIndexes()

        if len(selection_indexes) == 1:
            row = selection_indexes[0].row()
            col = selection_indexes[0].column()

            index_value = (row * self.ui.columns) + col

            potential_map_index = None

            for i in range(len(self.ui.potential_maps_start)):
                start = self.ui.potential_maps_start[i]
                end = self.ui.potential_maps_end[i]

                if start <= index_value <= end:
                    potential_map_index = i
                    break

            if potential_map_index is None:
                QMessageBox.warning(self.ui, "Warning", "There is no potential map on the selected cell!")
                return

            self.ui.potential_maps_start.pop(potential_map_index)
            self.ui.potential_maps_end.pop(potential_map_index)

            QMessageBox.information(self.ui, "Info", "Potential map has been successfully removed!")

            self.ui.sync_2d_scroll = True
            self.ui.mode2d.draw_canvas(self.ui)

    def start_potential_map_search(self, restart):
        if restart:
            if not self.ui.file_path:
                QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
                return
            reply = QMessageBox.question(
                self.ui,
                'Confirm Action',
                'Are you sure you want to start the potential map search?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                QMessageBox.information(self.ui, "Info", "Potential map search canceled.")
                return

        from potential_maps.potential_maps import Potential_maps_manager
        self.potential_maps_manager = Potential_maps_manager(self.ui)
        self.potential_maps_manager.find_potential_maps()

        if restart:
            self.ui.sync_2d_scroll = True
            self.ui.mode2d.draw_canvas(self.ui)