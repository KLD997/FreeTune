import math
import time
from tkinter import *
from tkinter import messagebox
import re
import numpy as np


class Mode3D:
    def __init__(self, ui):
        self.ui = ui

    def check_difference_3d(self, i, j):
        try:
            current_value = int(self.ui.entry_widgets[i][j].get())
            original_value = int(self.ui.original[i][j])
        except ValueError:
            return "break"

        difference = current_value - original_value
        self.ui.label_diff_3d.configure(text=f"Difference: {difference}")

    def copy_selected_cells(self):
        selected_content = ""
        for i in range(self.ui.rows_3d):
            row_content = ""
            for j in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[i][j]
                if entry.cget('bg') == 'lightblue':
                    row_content += entry.get() + "\t"
            if row_content:
                selected_content += row_content.strip() + "\n"
        selected_content = selected_content.strip()
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(selected_content)
        self.ui.update()

    def start_interaction(self, event, i, j):
        x, y = event.x_root, event.y_root
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
        self.selected_cells = {(i, j)}
        self.toggle_selection(i, j)
        self.highlight_cells()

    def start_interaction_x(self, event, j):
        x, y = event.x_root, event.y_root
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
        self.selected_cells = {(None, j)}
        self.highlight_cells()

    def start_interaction_y(self, event, i):
        x, y = event.x_root, event.y_root
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
        self.selected_cells = {(i, None)}
        self.highlight_cells()

    def end_interaction(self, event):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def drag_to_select(self, event):
        self.end_x = event.x_root
        self.end_y = event.y_root
        self.highlight_cells()

        if self.start_x == self.end_x and self.start_y == self.end_y:
            i, j = self.get_cell_index(self.start_x, self.start_y)
            if i is not None and j is not None:
                self.toggle_selection(i, j)

    def highlight_cells(self):
        if self.start_x is not None and self.start_y is not None:
            start_i, start_j = self.get_cell_index(self.start_x, self.start_y)
            if start_i is not None and start_j is not None:
                end_i, end_j = self.get_cell_index(self.end_x, self.end_y)
                if end_i is not None and end_j is not None:
                    min_i = min(start_i, end_i)
                    max_i = max(start_i, end_i)
                    min_j = min(start_j, end_j)
                    max_j = max(start_j, end_j)

                    for i in range(self.ui.rows_3d):
                        for j in range(self.ui.columns_3d):
                            entry = self.ui.entry_widgets[i][j]

                            if min_i <= i <= max_i and min_j <= j <= max_j:
                                if (i, j) not in self.selected_cells:
                                    entry.configure(bg="lightblue")
                            else:
                                if (i, j) in self.selected_cells:
                                    entry.configure(bg="lightblue")
                                else:
                                    entry.configure(bg="white")

    def toggle_selection(self, i, j):
        if (i, j) in self.selected_cells:
            self.selected_cells.remove((i, j))
            self.ui.entry_widgets[i][j].configure(bg="white")
        else:
            self.selected_cells.add((i, j))
            self.ui.entry_widgets[i][j].configure(bg="lightblue")

    def get_cell_index(self, x, y):
        for i in range(self.ui.rows_3d):
            for j in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[i][j]
                entry_x = entry.winfo_rootx()
                entry_y = entry.winfo_rooty()
                entry_width = entry.winfo_width()
                entry_height = entry.winfo_height()
                if entry_x <= x <= entry_x + entry_width and entry_y <= y <= entry_y + entry_height:
                    return i, j
        return None, None

    def increase_selected_text(self, int_value):
        try:
            increase_value = int_value
            for i in range(self.ui.rows_3d):
                for j in range(self.ui.columns_3d):
                    entry = self.ui.entry_widgets[i][j]
                    if entry.cget('bg') == 'lightblue':
                        current_value = int(entry.get())
                        new_value = current_value + increase_value
                        if 0 > new_value or new_value > 65535:
                            messagebox.showerror("Error", "Please enter a valid number")
                            return
                        new_value_str = '{:05d}'.format(new_value)
                        entry.delete(0, END)
                        entry.insert(END, new_value_str)
                        self.check_difference(event=None, i=i, j=j)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

        self.update_3d_view()

    def increase_selected_text_per(self, float_value):
        try:
            percentage_increase = float_value / 100.0
            for i in range(self.ui.rows_3d):
                for j in range(self.ui.columns_3d):
                    entry = self.ui.entry_widgets[i][j]
                    if entry.cget('bg') == 'lightblue':
                        current_value = int(entry.get())
                        increase_value = int(current_value * percentage_increase)
                        new_value = current_value + increase_value
                        if 0 > new_value or new_value > 65535:
                            messagebox.showerror("Error", "Please enter a valid number")
                            return
                        new_value_str = '{:05d}'.format(math.ceil(new_value))
                        entry.delete(0, END)
                        entry.insert(END, new_value_str)
                        self.check_difference(event=None, i=i, j=j)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid percentage.")
        self.update_3d_view()

    def set_text(self, int_value):
        try:
            set_text = int_value
            for i in range(self.ui.rows_3d):
                for j in range(self.ui.columns_3d):
                    entry = self.ui.entry_widgets[i][j]
                    if entry.cget('bg') == 'lightblue':
                        new_value = set_text
                        new_value_str = '{:05d}'.format(new_value)
                        entry.delete(0, END)
                        entry.insert(END, new_value_str)
                        self.check_difference(event=None, i=i, j=j)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        self.update_3d_view()

    def resize_grid(self, new_columns, new_rows):
        if new_rows > len(self.ui.entry_y_widgets):
            for x in range(len(self.ui.entry_y_widgets), new_rows):
                entry = Entry(self.ui.y_frame, width=5, font=("Comfortaa", 10))
                entry.grid(row=x, column=0)
                entry.insert(END, "00000")
                entry.bind('<KeyRelease>', lambda event, i=x: self.check_difference_y(event, i))
                entry.bind("<B1-Motion>", self.drag_to_select)
                entry.bind("<ButtonRelease-1>", self.end_interaction)
                self.ui.entry_y_widgets.append(entry)
                self.ui.original_Y.append("00000")
        elif new_rows < len(self.ui.entry_y_widgets):
            for i in range(len(self.ui.entry_y_widgets) - 1, new_rows - 1, -1):
                entry = self.ui.entry_y_widgets.pop()
                entry.destroy()
                self.ui.original_Y.pop()

        for i in range(new_rows):
            entry = self.ui.entry_y_widgets[i]
            entry.grid(row=i, column=0)

        if new_columns > len(self.ui.entry_x_widgets[0]):
            for x in range(len(self.ui.entry_x_widgets[0]), new_columns):
                entry = Entry(self.ui.x_frame, width=5, font=("Comfortaa", 10))
                entry.grid(row=0, column=x)
                entry.insert(END, "00000")
                entry.bind('<KeyRelease>', lambda event, j=x: self.check_difference_x(event, j))
                entry.bind("<ButtonPress-1>", lambda event, j=x: self.start_interaction_x(event, j))
                entry.bind("<B1-Motion>", self.drag_to_select)
                entry.bind("<ButtonRelease-1>", self.end_interaction)
                self.ui.entry_x_widgets[0].append(entry)
                self.ui.original_X[0].append("00000")
        elif new_columns < len(self.ui.entry_x_widgets[0]):
            for j in range(len(self.ui.entry_x_widgets[0]) - 1, new_columns - 1, -1):
                entry = self.ui.entry_x_widgets[0].pop()
                entry.destroy()
                self.ui.original_X[0].pop()

        if new_rows > len(self.ui.entry_widgets):
            for x in range(len(self.ui.entry_widgets), new_rows):
                row = []
                original_row = []
                for y in range(new_columns):
                    entry = Entry(self.ui.main_frame, width=5, font=("Comfortaa", 10))
                    entry.grid(row=x, column=y)
                    entry.insert(END, "00000")
                    entry.bind('<KeyRelease>', lambda event, i=x, j=y: self.check_difference(event, i, j))
                    entry.bind("<ButtonPress-1>", lambda event, i=x, j=y: (
                        self.start_interaction(event, i, j), self.check_difference_3d(i, j)))
                    entry.bind("<B1-Motion>", self.drag_to_select)
                    entry.bind("<ButtonRelease-1>", self.end_interaction)
                    row.append(entry)
                    original_row.append("00000")
                self.ui.entry_widgets.append(row)
                self.ui.original.append(original_row)
        elif new_rows < len(self.ui.entry_widgets):
            for i in range(len(self.ui.entry_widgets) - 1, new_rows - 1, -1):
                row = self.ui.entry_widgets.pop()
                for entry in row:
                    entry.destroy()
                self.ui.original.pop()

        for x in range(len(self.ui.entry_widgets)):
            row = self.ui.entry_widgets[x]
            original_row = self.ui.original[x]
            for y in range(len(row), new_columns):
                entry = Entry(self.ui.main_frame, width=5, font=("Comfortaa", 10))
                entry.grid(row=x, column=y)
                entry.insert(END, "00000")
                entry.bind('<KeyRelease>', lambda event, i=x, j=y: self.check_difference(event, i, j))
                entry.bind("<ButtonPress-1>", lambda event, i=x, j=y: (
                self.start_interaction(event, i, j), self.check_difference_3d(i, j)))
                entry.bind("<B1-Motion>", self.drag_to_select)
                entry.bind("<ButtonRelease-1>", self.end_interaction)
                row.append(entry)
                original_row.append("00000")
            for j in range(len(row) - 1, new_columns - 1, -1):
                entry = row.pop()
                entry.destroy()
                original_row.pop()

        self.ui.columns_3d = new_columns
        self.ui.rows_3d = new_rows

    def update_3d_view(self):
        try:
            x_default = all(entry.get() == "00000" for entry in self.ui.entry_x_widgets[0])
            y_default = all(entry.get() == "00000" for entry in self.ui.entry_y_widgets)

            if x_default and y_default:
                x = np.arange(self.ui.columns_3d)
                y = np.arange(self.ui.rows_3d)
                x, y = np.meshgrid(x, y)

                values = np.zeros((self.ui.rows_3d, self.ui.columns_3d))
                for i in range(self.ui.rows_3d):
                    for j in range(self.ui.columns_3d):
                        value = float(self.ui.entry_widgets[i][j].get())
                        values[i][j] = value

                self.ui.ax_3d.clear()
                surf = self.ui.ax_3d.plot_surface(x, y, values, cmap='viridis', edgecolor='none')
                self.ui.ax_3d.set_xlabel('X')
                self.ui.ax_3d.set_ylabel('Y')
                self.ui.ax_3d.set_zlabel('Value')

                self.ui.ax_3d.set_xticks([])
                self.ui.ax_3d.set_yticks([])

                self.ui.canvas_3d.draw()
            else:
                x = np.arange(self.ui.columns_3d)
                y = np.arange(self.ui.rows_3d)
                x, y = np.meshgrid(x, y)

                values = np.zeros((self.ui.rows_3d, self.ui.columns_3d))
                for i in range(self.ui.rows_3d):
                    for j in range(self.ui.columns_3d):
                        value = float(self.ui.entry_widgets[i][j].get())
                        values[i][j] = value

                self.ui.ax_3d.clear()
                self.ui.ax_3d.plot_surface(x, y, values, cmap='viridis')
                self.ui.ax_3d.set_xlabel('X')
                self.ui.ax_3d.set_ylabel('Y')
                self.ui.ax_3d.set_zlabel('Value')

                self.ui.ax_3d.set_xticks(np.arange(0, self.ui.columns_3d, 1))
                self.ui.ax_3d.set_yticks(np.arange(0, self.ui.rows_3d, 1))

                self.ui.canvas_3d.draw()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def paste_data(self, maps, data, row, col, new):
        if maps:
            self.resize_grid(col, row)
            index = 0
            for i in range(row):
                for j in range(col):
                    self.ui.entry_widgets[i][j].delete(0, END)
                    self.ui.entry_widgets[i][j].insert(0, f"{data[index]:05}")
                    if not new:
                        self.ui.original[i][j] = data[index]
                    index += 1
                    self.ui.entry_widgets[i][j].configure(fg="black")
            self.ui.rows_entry.configure(state="normal")
            self.ui.columns_entry.configure(state="normal")
            self.ui.rows_entry.delete(0, END)
            self.ui.rows_entry.insert(0, f"{row:02}")
            self.ui.columns_entry.delete(0, END)
            self.ui.columns_entry.insert(0, f"{col:02}")
            self.ui.rows_entry.configure(state="disabled")
            self.ui.columns_entry.configure(state="disabled")
        else:
            data = self.ui.window.clipboard_get()
            lines = data.strip().split('\n')
            num_rows = len(lines)
            num_columns = max(len(line.strip().split('\t')) for line in lines)
            try:
                self.ui.rows_entry.configure(state="normal")
                self.ui.columns_entry.configure(state="normal")
                self.ui.rows_entry.delete(0, END)
                self.ui.rows_entry.insert(0, f"{num_rows:02}")
                self.ui.columns_entry.delete(0, END)
                self.ui.columns_entry.insert(0, f"{num_columns:02}")
                self.ui.rows_entry.configure(state="disabled")
                self.ui.columns_entry.configure(state="disabled")

                self.clear_highlighting()

                self.resize_grid(num_columns, num_rows)

                for i, line in enumerate(lines):
                    numbers = line.strip().split('\t')
                    for j, num in enumerate(numbers):
                        if i < self.ui.rows_3d and j < self.ui.columns_3d:
                            new_value = '{:05d}'.format(int(num))
                            self.ui.entry_widgets[i][j].delete(0, END)
                            self.ui.entry_widgets[i][j].insert(0, new_value)
                            if not new:
                                self.ui.original[i][j] = new_value
                            self.ui.entry_widgets[i][j].configure(fg="black")

                last_row_values = [entry.get() for entry in self.ui.entry_widgets[-1]]
                if not any(last_row_values) and self.ui.rows_3d > 1:
                    last_row = self.ui.entry_widgets.pop()
                    for entry in last_row:
                        entry.destroy()
                    num_rows -= 1
                    self.ui.rows_entry.configure(state="normal")
                    self.ui.rows_entry.delete(0, END)
                    self.ui.rows_entry.insert(0, f"{num_rows:02}")
                    self.ui.rows_entry.configure(state="disabled")

            except TclError:
                messagebox.showerror("Error", "Clipboard operation failed. Please try again.")

        self.update_3d_view()

    def paste_x_data(self, maps, data, new):
        if maps:
            for i in range(len(data)):
                self.ui.entry_x_widgets[0][i].delete(0, END)
                self.ui.entry_x_widgets[0][i].insert(0, f"{data[i]:05}")
                if not new:
                    self.ui.original_X[0][i] = data[i]
                self.check_difference_x(None, i)

        else:
            data = self.ui.window.clipboard_get()
            try:
                numbers = data.strip().split('\t')

                self.clear_highlighting()

                for j, num in enumerate(numbers):
                    if j < self.ui.columns_3d:
                        new_value = '{:05d}'.format(int(num))
                        self.ui.entry_x_widgets[0][j].delete(0, END)
                        self.ui.entry_x_widgets[0][j].insert(0, new_value)
                        if not new:
                            self.ui.original_X[0][j] = new_value

            except TclError:
                messagebox.showerror("Error", "Clipboard operation failed. Please try again.")

            self.update_3d_view()

    def paste_y_data(self, maps, data, new):
        if maps:
            for i in range(len(data)):
                self.ui.entry_y_widgets[i].delete(0, END)
                self.ui.entry_y_widgets[i].insert(0, f"{data[i]:05}")
                if not new:
                    self.ui.original_Y[i] = data[i]
                self.check_difference_y(None, i)
        else:
            data = self.ui.window.clipboard_get()
            try:
                numbers = re.split(r'\s+', data.strip())

                self.clear_highlighting()

                for i, num in enumerate(numbers):
                    if i < len(self.ui.entry_y_widgets):
                        try:
                            new_value = '{:05d}'.format(int(num))
                            self.ui.entry_y_widgets[i].delete(0, END)
                            self.ui.entry_y_widgets[i].insert(0, new_value)
                            if i < len(self.ui.original_Y):
                                if not new:
                                    self.ui.original_Y[i] = new_value
                        except ValueError:
                            messagebox.showerror("Error", f"Invalid value '{num}' found in clipboard data.")
                            continue
                    else:
                        messagebox.showwarning("Warning", "More data in clipboard than available entry widgets.")


            except TclError:
                messagebox.showerror("Error", "Clipboard operation failed. Please try again.")

        self.update_3d_view()

    def clear_highlighting(self):
        for i in range(self.ui.rows_3d):
            for j in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[i][j]
                entry.configure(bg="white")

    def check_difference(self, event, i, j):
        entry = self.ui.entry_widgets[i][j]
        original_value = int(self.ui.original[i][j])

        if len(entry.get()) > 5:
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)

        try:
            current_value = int(entry.get())
        except ValueError:
            current_index = entry.index(INSERT)
            entry.delete(current_index - 1, current_index)
            return

        if current_value > original_value:
            entry.configure(fg="red")
        elif current_value < original_value:
            entry.configure(fg="blue")
        else:
            entry.configure(fg="black")

        time.sleep(0.01)

        self.update_3d_view()

    def check_difference_x(self, event, j):
        entry = self.ui.entry_x_widgets[0][j]
        original_value = int(self.ui.original_X[0][j])
        try:
            current_value = int(entry.get())
        except ValueError:
            return

        if current_value > original_value:
            entry.configure(fg="red")
        elif current_value < original_value:
            entry.configure(fg="blue")
        else:
            entry.configure(fg="black")

        time.sleep(0.01)

        self.clear_highlighting()
        self.update_3d_view()

    def check_difference_y(self, event, i):
        entry = self.ui.entry_y_widgets[i]
        original_value = int(self.ui.original_Y[i])
        try:
            current_value = int(entry.get())
        except ValueError:
            return

        if current_value > original_value:
            entry.configure(fg="red")
        elif current_value < original_value:
            entry.configure(fg="blue")
        else:
            entry.configure(fg="black")

        time.sleep(0.01)

        self.clear_highlighting()
        self.update_3d_view()

    def copy_map_values(self):
        map_values = ""
        for i in range(self.ui.rows_3d):
            for j in range(self.ui.columns_3d):
                map_values += self.ui.entry_widgets[i][j].get() + "\t"
            map_values += "\n"
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(map_values)

    def copy_x_axis(self):
        x_axis_values = "\t".join(entry.get() for entry in self.ui.entry_x_widgets[0])
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(x_axis_values)

    def copy_y_axis(self):
        y_axis_values = "\n".join(entry.get() for entry in self.ui.entry_y_widgets)
        self.ui.window.clipboard_clear()
        self.ui.window.clipboard_append(y_axis_values)

    def check_all(self):
        for row in range(self.ui.rows_3d):
            for col in range(self.ui.columns_3d):
                self.check_difference(None, row, col)

        for col in range(self.ui.columns_3d):
            self.check_difference_x(None, col)

        for row in range(self.ui.rows_3d):
            self.check_difference_y(None, row)

    def on_focus_out(self, event, row, col, mode):
        if mode == "map":
            entry = self.ui.entry_widgets[row][col]
            if len(entry.get()) == 0:
                entry.insert(END, f"{self.ui.original[row][col]:05}")
            else:
                int_value = int(entry.get())
                entry.delete(0, END)
                entry.insert(END, f"{int_value:05}")
                self.check_difference(None, row, col)
            if entry.selection_present():
                entry.selection_clear()
        if mode == "x":
            entry = self.ui.entry_x_widgets[row][col]
            if len(entry.get()) == 0:
                entry.insert(END, f"{self.ui.original_X[row][col]:05}")
            else:
                int_value = int(entry.get())
                entry.delete(0, END)
                entry.insert(END, f"{int_value:05}")
                self.check_difference_x(None, col)
            if entry.selection_present():
                entry.selection_clear()
        if mode == "y":
            entry = self.ui.entry_y_widgets[row]
            if len(entry.get()) == 0:
                entry.insert(END, f"{self.ui.original_Y[row]:05}")
            else:
                int_value = int(entry.get())
                entry.delete(0, END)
                entry.insert(END, f"{int_value:05}")
                self.check_difference_y(None, row)
            if entry.selection_present():
                entry.selection_clear()

    def select_all(self, event, row, col, mode):
        if mode in ("map", "x", "y"):
            if mode == "map":
                entry = self.ui.entry_widgets[row][col]
            elif mode == "x":
                entry = self.ui.entry_x_widgets[row][col]
            else:
                entry = self.ui.entry_y_widgets[row]

            entry.select_range(0, END)
            entry.icursor(END)
        return "break"

    def clear_highlight_on_tab(self, event):
        self.clear_highlighting()

    def set_default(self):
        self.resize_grid(10, 10)
        for row in range(self.ui.rows_3d):
            for col in range(self.ui.columns_3d):
                entry = self.ui.entry_widgets[row][col]
                entry.delete(0, END)
                entry.insert(END, "00000")
                self.ui.original[row][col] = 0

        for col in range(self.ui.columns_3d):
            entry = self.ui.entry_x_widgets[0][col]
            entry.delete(0, END)
            entry.insert(END, "00000")
            self.ui.original_X[0][col] = 0

        for row in range(self.ui.rows_3d):
            entry = self.ui.entry_y_widgets[row]
            entry.delete(0, END)
            entry.insert(END, "00000")
            self.ui.original_Y[row] = 0

        self.ui.columns_entry.configure(state="normal")
        self.ui.rows_entry.configure(state="normal")

        self.ui.rows_entry.delete(0, END)
        self.ui.columns_entry.delete(0, END)
        self.ui.rows_entry.insert(END, str(self.ui.rows_3d))
        self.ui.columns_entry.insert(END, str(self.ui.columns_3d))

        self.ui.columns_entry.configure(state="disabled")
        self.ui.rows_entry.configure(state="disabled")

        self.update_3d_view()