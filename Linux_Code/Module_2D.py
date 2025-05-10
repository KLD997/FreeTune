import numpy as np
import time
from PyQt6.QtCore import QItemSelectionModel
from PyQt6.QtWidgets import QMessageBox, QTableView

class Mode2D:
    def __init__(self, ui):
        self.ui = ui
        self.last_page_change_time = 0
        self.is_dragging = False
        self.last_x = 0
        self.highlight_enabled = False

    def scale_to_fixed_range(self, data, min_val=0, max_val=65535):
        return [min(max(val, min_val), max_val) for val in data]

    def draw_canvas(self, ui):
        self.ui = ui

        if self.ui.disable_2d_canvas:
            return

        self.ui.ax.clear()

        start_index = self.ui.current_frame + self.ui.shift_count
        end_index_mod = min(start_index + self.ui.num_rows * self.ui.columns, len(self.ui.current_values)) + self.ui.shift_count
        data_unpacked_mod = self.ui.current_values[start_index:end_index_mod]

        data_unpacked = self.ui.unpacked[start_index - self.ui.shift_count:end_index_mod - self.ui.shift_count]

        scaled_data_mod = self.scale_to_fixed_range(data_unpacked_mod)
        scaled_data = self.scale_to_fixed_range(data_unpacked)

        scaled_data_mod = np.array(scaled_data_mod)
        scaled_data = np.array(scaled_data)

        mask = scaled_data_mod != scaled_data

        self.ui.ax.plot(scaled_data, color="white", linewidth=0.5)

        if np.any(mask):
            differing_indices = np.where(mask)[0]
            segments = np.split(differing_indices, np.where(np.diff(differing_indices) != 1)[0] + 1)

            for segment in segments:
                # Expand segment to include one value before and after, safely
                start = max(segment[0] - 1, 0)
                end = min(segment[-1] + 2, len(scaled_data_mod))  # +2 because slicing is exclusive at the end
                extended_segment = np.arange(start, end)

                self.ui.ax.plot(extended_segment, scaled_data_mod[extended_segment], color="red", linewidth=0.5)

        if self.ui.red_line is not None:
            self.ui.ax.axvline(self.ui.red_line, color="#bd090e", linestyle='-', label="Clicked Position")

        if self.ui.display_sel:
            self.ui.ax.axvspan(self.ui.sel_start, self.ui.sel_end, color="#555", alpha=0.3, label="Selected Area")

        start_maps = self.ui.start_index_maps
        end_maps = self.ui.end_index_maps
        frame = self.ui.num_rows * self.ui.columns

        # User created maps

        for i in range(len(self.ui.start_index_maps)):
            start = start_maps[i] + self.ui.shift_count
            end = end_maps[i] + self.ui.shift_count

            new_start = start - start_index
            new_end = end - start_index

            if 0 <= new_start <= frame and 0 <= new_end <= frame:
                self.ui.ax.axvspan(new_start, new_end, color="#85d7f2", alpha=0.3, label=f"{self.ui.maps_names[i]}")

        # Display -> Potential maps

        start_maps = self.ui.potential_maps_start
        end_maps = self.ui.potential_maps_end

        found_maps = False

        for i in range(len(self.ui.potential_maps_start)):
            start = start_maps[i]
            end = end_maps[i]

            new_start = start - start_index
            new_end = end - start_index

            if 0 <= new_end <= frame and 0 <= new_start <= frame:
                self.ui.ax.axvspan(new_start, new_end, color="#01857b", alpha=0.3,
                                    label=f"{self.ui.potential_maps_names[i]}")
                found_maps = True
            else:
                if found_maps:
                    break

        if not self.highlight_enabled and not self.ui.display_sel and not self.ui.sync_2d_scroll: # calibrate text to 2d
            row = (start_index - self.ui.shift_count) // self.ui.columns
            index_sel = self.ui.model.index(row, 0)
            self.ui.table_view.scrollTo(index_sel, QTableView.ScrollHint.PositionAtCenter)

            selection_model = self.ui.table_view.selectionModel()
            selection_model.clearSelection()

        self.ui.ax.set_xlim(0, len(scaled_data_mod))
        self.ui.ax.set_ylim(0, 65535)

        self.ui.ax.axis('off')
        self.ui.ax.grid(True, which='both', color='white', linestyle='-', linewidth=0.5)

        self.ui.canvas.draw()

        if self.ui.return_text:
            self.ui.return_text = False
        self.ui.display_sel = False
        self.highlight_enabled = False

    def on_canvas_click(self, event):
        if not self.ui.unpacked:
            return
        x_pos = event.xdata
        if x_pos is not None:
            self.ui.display_sel = False
            self.ui.red_line = int(x_pos)
            self.highlight_text(self.ui.red_line, False)
            self.draw_canvas(self.ui)

    def highlight_text(self, x, find_on):
        x += self.ui.shift_count
        if self.ui.current_frame > 0 and not find_on:
            value_index = x + self.ui.current_frame
        else:
            value_index = x

        self.ui.table_view.clearSelection()

        row = value_index // self.ui.columns
        col = (value_index % self.ui.columns)
        # scroll to highlight
        index_sel = self.ui.model.index(row, col)
        self.ui.table_view.scrollTo(index_sel, QTableView.ScrollHint.PositionAtCenter)

        index = self.ui.model.index(row, col)
        selection_model = self.ui.table_view.selectionModel()
        selection_model.select(index, QItemSelectionModel.SelectionFlag.Select)

        if not find_on:
            value = self.ui.current_values[x + self.ui.current_frame]
        else:
            value = self.ui.current_values[x]

        self.ui.value_btn_2d.setText(f"Value: {value:05}")

        self.highlight_enabled = True

    def prev_page(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        current_time = time.time()
        if current_time - self.last_page_change_time < 0.12:
            return
        if self.ui.current_frame - self.ui.num_rows * self.ui.columns >= 0:
            self.ui.red_line = None
            self.ui.current_frame -= self.ui.num_rows * self.ui.columns
            self.draw_canvas(self.ui)

    def next_page(self):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        current_time = time.time()
        if current_time - self.last_page_change_time < 0.12:
            return
        if self.ui.current_frame + self.ui.num_rows * self.ui.columns < len(self.ui.unpacked):
            self.ui.red_line = None
            self.ui.current_frame += self.ui.num_rows * self.ui.columns
            self.draw_canvas(self.ui)

    def fast_movement(self, direction):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        current_time = time.time()
        if current_time - self.last_page_change_time < 0.12:
            return
        self.ui.red_line = None
        if direction == "right":
            if self.ui.current_frame + 200 < len(self.ui.unpacked):
                self.ui.current_frame += 200
                self.draw_canvas(self.ui)
        elif direction == "left":
            self.ui.current_frame -= 200
            if self.ui.current_frame > 0:
                self.draw_canvas(self.ui)
            else:
                self.ui.current_frame = 0
                self.draw_canvas(self.ui)

    def percentage(self, entry, arg):
        if not self.ui.file_path:
            QMessageBox.warning(self.ui, "Warning", "No file is currently open. Please open a file first.")
            return

        if entry:
            try:
                num = int(self.ui.entry_percentage.text())
                if num < 0 or num > 100:
                    raise ValueError
                self.ui.percentage_num = num
                self.ui.entry_percentage.setText(f"{self.ui.percentage_num:02}")
            except ValueError:
                QMessageBox.warning(self.ui, "Warning", "Enter a correct value! (0% - 100%)")
                return
        else:
            if arg == "+" and self.ui.percentage_num < 99:
                self.ui.percentage_num += 1
                num = self.ui.percentage_num
                self.ui.entry_percentage.setText(f"{self.ui.percentage_num:02}")
            elif arg == "-" and self.ui.percentage_num > 0:
                self.ui.percentage_num -= 1
                num = self.ui.percentage_num
                self.ui.entry_percentage.setText(f"{self.ui.percentage_num:02}")
            else:
                num = 0
        if 0 <= num <= 100:
            self.ui.red_line = None
            self.ui.current_frame = int((len(self.ui.unpacked) - self.ui.num_rows * self.ui.columns) * (num / 100))
            self.draw_canvas(self.ui)

    def text_to_2d(self, ui):
        if not self.ui.text_addons.check_selection_consecutive():
            QMessageBox.warning(self.ui, "Warning", "Data selection is not correct!")
            return

        self.ui = ui
        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        selected_indexes_count = len(selection_model.selectedIndexes())

        if selected_indexes_count == 1:
            self.ui.display_sel = False
            item = selected_indexes[0]
            row = item.row()  # current row
            col = item.column()  # current column

            index = row * self.ui.columns + col - self.ui.shift_count
            frame = self.ui.num_rows * self.ui.columns
            frames_num = index // frame
            self.ui.current_frame = frames_num * frame

            self.ui.red_line = int(index) - self.ui.current_frame

            self.highlight_text(index, True)

            value = self.ui.current_values[index + self.ui.shift_count]
            self.ui.value_btn_2d.setText(f"Value: {value:05}")

        if selected_indexes_count > 1:
            first_item = selected_indexes[0]

            first_row = first_item.row()
            first_col = first_item.column()

            index = first_row * self.ui.columns + first_col - self.ui.shift_count
            frame = self.ui.num_rows * self.ui.columns
            frames_num = index // frame
            self.ui.current_frame = frames_num * frame

            if self.ui.current_frame > 0:
                self.ui.sel_start = int(index) - self.ui.current_frame
            else:
                self.ui.sel_start = int(index)

            self.ui.red_line = int(index) - self.ui.current_frame

            self.ui.sel_end = self.ui.sel_start + selected_indexes_count - 1

            self.ui.display_sel = True

            self.ui.value_btn_2d.setText(f"Value: 00000")

        self.draw_canvas(self.ui)

    def on_key_press_2d(self, event): # change later
        pressed_key = event.key

        if pressed_key == "n":
            self.value_changes_skipping(True)
        if pressed_key == "v":
            self.value_changes_skipping(False)
        if pressed_key == "pageup":
            self.next_page()
        if pressed_key == "pagedown":
            self.prev_page()

    def value_changes_skipping(self, forward):
        selection_model = self.ui.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        found_value_index = None

        selected_index = selected_indexes[0]

        if not selected_indexes:
            QMessageBox.warning(self.ui, "Warning", "Please select a number!")
            return

        row = selected_index.row()
        col = selected_index.column()

        index = (row * self.ui.columns) + col

        if forward:
            for i in range(index + 1, len(self.ui.current_values)):
                if self.ui.current_values[i] != self.ui.unpacked[i - self.ui.shift_count] and self.ui.current_values[i] is not None:
                    found_value_index = i
                    while self.ui.current_values[i] != self.ui.unpacked[i - self.ui.shift_count] and self.ui.current_values[i] is not None:
                        found_value_index += 1
                        i += 1
                    found_value_index -= 1
                    break
        else:
            for i in range(index - 1, -1, -1):
                if self.ui.current_values[i] != self.ui.unpacked[i - self.ui.shift_count] and self.ui.current_values[i] is not None:
                    found_value_index = i
                    while self.ui.current_values[i] != self.ui.unpacked[i - self.ui.shift_count] and self.ui.current_values[i] is not None:
                        found_value_index -= 1
                        i -= 1
                    found_value_index += 1
                    break

        if found_value_index is None:
            QMessageBox.warning(self.ui, "Warning", "No values found!")
            return

        self.ui.mode2d.highlight_text(found_value_index - self.ui.shift_count, True)
        self.ui.mode2d.text_to_2d(self.ui)
