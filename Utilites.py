from tkinter import *
from tkinter import messagebox
import time
from text_view import TextView

class Utility:
    def __init__(self, ui):
        self.ui = ui
        self.text_view = TextView(self)

    def copy_values(self):
        selected_text = self.ui.text_widget.selection_get()
        if not selected_text:
            messagebox.showwarning("Nothing Selected", "No values are selected to copy.")
            return

        selected_values = selected_text.strip().split()

        num_rows = len(selected_values) // self.ui.columns
        if len(selected_values) % self.ui.columns != 0:
            num_rows += 1

        copied_content = ""
        for i in range(num_rows):
            start_index = i * self.ui.columns
            end_index = min((i + 1) * self.ui.columns, len(selected_values))
            row_values = selected_values[start_index:end_index]
            copied_content += "\t".join(row_values) + "\n"

        try:
            self.ui.window.clipboard_clear()
            self.ui.window.clipboard_append(copied_content)
        except Exception as e:
            messagebox.showerror("Copy Error", f"An error occurred while copying: {e}")

    def paste_values(self, ui):
        self.ui = ui
        selected_text = self.ui.window.clipboard_get()
        cleaned_values = selected_text.strip().split()

        cursor_index = self.ui.text_widget.index(INSERT)
        cursor_row, cursor_col = map(int, cursor_index.split('.'))

        current_content = self.ui.text_widget.get(1.0, END)
        current_lines = current_content.strip().split('\n')

        row_index = cursor_row - 1
        col_index = cursor_col // 6

        differences = []

        for value in cleaned_values:
            if row_index >= len(current_lines):
                break

            current_line = current_lines[row_index]
            values = current_line.split()

            if col_index >= len(values):
                row_index += 1
                col_index = 0
                if row_index >= len(current_lines):
                    break
                current_line = current_lines[row_index]
                values = current_line.split()

            if values[col_index] != value:
                differences.append((values[col_index], value, row_index, col_index))

            values[col_index] = value

            current_lines[row_index] = ' '.join(values)

            col_index += 1

        updated_content = '\n'.join(current_lines)
        self.ui.text_widget.delete(1.0, END)
        self.ui.text_widget.insert(END, updated_content)

        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        int_values = [int(x) for x in self.ui.current_values]
        self.check_difference_values(int_values, True, self.ui)
        self.ui.text_widget.see(cursor_index)

    def check_difference_values(self, new_values, importing, ui):
        self.ui = ui
        self.ui.differences = {}
        self.ui.differences_color = {}
        self.ui.ori_values = {}
        self.ui.index_differences = {}

        if importing:
            first_visible_row = 0
            last_visible_row = int(len(self.ui.unpacked) / self.ui.columns)
        else:
            first_visible_row = int(self.ui.text_widget.yview()[0] * self.ui.total_rows)
            last_visible_row = int(self.ui.text_widget.yview()[1] * self.ui.total_rows)

        index = (self.ui.columns * first_visible_row) - 1
        counter = -1

        for row in range(first_visible_row, last_visible_row):
            for col in range(0, self.ui.columns):
                index += 1
                shifted_col = (col + self.ui.shift_count) % self.ui.columns
                row_shift = (col + self.ui.shift_count) // self.ui.columns
                current_row = row + row_shift

                start_index = f"{current_row + 1}.{shifted_col * 6}"
                end_index = f"{current_row + 1}.{(shifted_col + 1) * 6 - 1}"

                self.ui.text_widget.tag_remove("changed_red", start_index, end_index)
                self.ui.text_widget.tag_remove("changed_blue", start_index, end_index)

                if self.ui.unpacked[index] < new_values[index]:
                    counter += 1
                    self.ui.text_widget.tag_add("changed_red", start_index, end_index)
                    self.ui.text_widget.tag_configure("changed_red", foreground="#ed7d80")
                    self.ui.differences[counter] = new_values[index]
                    self.ui.ori_values[counter] = self.ui.unpacked[index]
                    self.ui.differences_color[counter] = "red"
                    self.ui.index_differences[counter] = index
                elif self.ui.unpacked[index] > new_values[index]:
                    counter += 1
                    self.ui.text_widget.tag_add("changed_blue", start_index, end_index)
                    self.ui.text_widget.tag_configure("changed_blue", foreground="#65a1e6")
                    self.ui.differences[counter] = new_values[index]
                    self.ui.ori_values[counter] = self.ui.unpacked[index]
                    self.ui.differences_color[counter] = "blue"
                    self.ui.index_differences[counter] = index

    def adjust_columns(self, ui):
        self.ui = ui
        entry_content = self.ui.entry.get()
        try:
            value = int(entry_content)
        except ValueError:
            return
        if value < 0 or value > 60:
            return
        self.ui.columns = value

        self.ui.entry.delete(0, END)
        self.ui.entry.insert(END, str(self.ui.columns))

        max_frame = max(0, len(self.ui.unpacked) - self.ui.num_rows * self.ui.columns)
        self.ui.current_frame = min(self.ui.current_frame, max_frame)

        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()

        self.ui.text_widget.delete(1.0, END)

        for i in range(self.ui.total_rows):
            row = self.ui.current_values[i * self.ui.columns:(i + 1) * self.ui.columns]
            formatted = ' '.join(f"{value:05}" for value in row)
            self.ui.text_widget.insert(END, formatted + '\n')
        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        new_values = self.ui.current_values[self.ui.shift_count:]
        self.ui.current_values = new_values

        int_values = [int(x) for x in self.ui.current_values]
        new_values = int_values[self.ui.shift_count:]
        self.check_difference_values(new_values, False, self.ui)

        from text_view import TextView
        from Module_2D import Mode2D
        self.text_view = TextView(self)
        self.mode2d = Mode2D(self)

        self.ui.return_text = True

        self.mode2d.draw_canvas(self.ui)
        self.ui.window.update_idletasks()


    def check_value_changes(self, ui):
        self.ui = ui
        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        int_values = [int(x) for x in self.ui.current_values]
        new_values = int_values[self.ui.shift_count:]
        self.check_difference_values(new_values, False, self.ui)

    def move_items(self, ui):
        self.ui = ui
        self.ui.end_time = time.time()
        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
        int_values = [int(x) for x in self.ui.current_values]
        new_values = int_values[self.ui.shift_count:]
        if ((self.ui.end_time - self.ui.start_time) > 0.2):
            try:
                value = int(self.ui.entry_position.get())
            except ValueError:
                return
            if value < 0 or value > 60:
                return
            self.ui.shift_count = value
            self.ui.entry_position.delete(0, END)
            self.ui.entry_position.insert(0, f"{self.ui.shift_count:02}")
            if self.ui.shift_count < self.ui.columns:
                self.ui.values = []
                self.ui.text_widget.delete(1.0, END)
                for i in range(self.ui.shift_count):
                    self.ui.values.append(0)
                self.ui.values += new_values
                rows = [self.ui.values[i:i + self.ui.columns] for i in range(0, len(self.ui.values), self.ui.columns)]
                for row in rows:
                    formatted = ' '.join(f"{value:05}" for value in row)
                    self.ui.text_widget.insert(END, formatted + '\n')
            self.ui.start_time = time.time()
        self.check_difference_values(new_values, True, self.ui)

        from Module_2D import Mode2D
        self.mode2d = Mode2D(self)
        self.ui.return_text = True
        self.mode2d.draw_canvas(self.ui)

    def undo(self):
        self.ui.text_widget.edit_undo()
        self.check_value_changes(self.ui)

    def redo(self):
        self.ui.text_widget.edit_redo()
        self.check_value_changes(self.ui)