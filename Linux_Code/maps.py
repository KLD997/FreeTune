import os
from tkinter import *
from tkinter import messagebox
import subprocess

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
        from Utilities import Utility
        utility = Utility(self.ui)
        utility.copy_values()
        if utility.nothing_selected:
            return
        data = self.ui.window.clipboard_get()
        self.start_index = utility.start_selection - self.ui.shift_count
        self.end_index = utility.end_selection - self.ui.shift_count + 1
        self.ui.text_widget.tag_remove(SEL, "1.0", END)
        map_data = data.strip().split()
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
        factor_dialog = Toplevel(bg="#333")
        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()

        width = 250
        height = 120
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        factor_dialog.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        factor_dialog.title("Map Creator")

        label = Label(factor_dialog, text="Select a factor:", bg="#333", fg="white")
        label.pack(pady=5)
        self.factor_list = Listbox(factor_dialog, bg="#333", fg="white")
        self.factor_list.pack(fill=BOTH, expand=YES)

        self.factor_dialog_window = factor_dialog

        for i in range(0, len(factors), 2):
            self.factor_list.insert(i, f"{factors[i]}x{int(factors[i + 1])}")

        self.factor_list.bind('<Double-Button-1>', self.factor_select)

    def factor_select(self, event):
        selected = self.factor_list.curselection()
        item = self.factor_list.get(selected[0])
        self.size = item
        self.factor_dialog_window.destroy()
        self.dialog_name()

    def dialog_name(self):
        dialog_name = Toplevel(bg="#333")
        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()

        self.dialog_name_window = dialog_name

        width = 250
        height = 100
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        dialog_name.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        dialog_name.title("Map Creator")

        label = Label(dialog_name, text="Name your map:", bg="#333", fg="white", font=8)
        label.pack(pady=5)
        self.name_entry = Entry(dialog_name, bg="#555", fg="white", highlightthickness=0)
        self.name_entry.pack(pady=5)
        btn = Button(dialog_name, bg="#444", fg="white", text="Create", highlightthickness=0, command=self.create_map)
        btn.pack(pady=5)

    def create_map(self):
        map_name = self.name_entry.get()
        if map_name == "":
            return
        self.map_name = map_name
        if not self.first_run:
            with open(self.file_path, 'r') as file:
                content = file.read().split('\n')
                for i in range(len(content)):
                    if content[i] == self.map_name:
                        messagebox.showerror("Error", "This name is already in use! Choose a new one!")
                        return

        self.first_run = False
        self.dialog_name_window.destroy()
        self.ui.map_list.insert(self.ui.map_list_counter, self.map_name)
        self.ui.maps_names.append(self.map_name)
        self.highlight_text_map(self.start_index, self.end_index)
        self.highlight_2d_map(self.start_index, self.end_index)
        self.write_file_mp()
        self.ui.map_list_counter += 1

    def write_file_mp(self):
        with open(self.file_path, 'a') as file:
            file.write(f"\n{self.map_name}\n" if self.ui.map_list_counter > 0 else f"{self.map_name}\n")
            file.write(f"{self.start_index}\n")
            file.write(f"{self.end_index}\n")
            file.write(f"{self.size}")

    def on_double_click(self, event):
        selection = self.ui.map_list.curselection()
        if not selection:
            return
        self.double_click = True
        index = selection[0]
        self.last_map_index = index
        self.update_3d_from_text()

    def update_3d_from_text(self):
        item = self.ui.map_list.get(self.last_map_index)
        with open(self.file_path, 'r') as file:
            content = file.read().split("\n")
            for i in range(len(content)):
                if content[i] == item:
                    start_index = int(content[i + 1])
                    end_index = int(content[i + 2])
                    size = content[i + 3]

                    parts = size.split('x')
                    self.col = int(parts[0])
                    self.row = int(parts[1])

                    from Module_3D import Mode3D
                    mode3d = Mode3D(self.ui)

                    self.map_data = self.ui.unpacked[start_index:end_index]
                    mode3d.paste_data(True, self.map_data, self.row, self.col, False)
                    if not (start_index - (self.col + self.row) < 0):
                        self.x_axis = self.ui.unpacked[start_index - self.col:start_index]
                        self.y_axis = self.ui.unpacked[start_index - (self.col + self.row):start_index - self.col]
                        mode3d.paste_x_data(True, self.x_axis, False)
                        mode3d.paste_y_data(True, self.y_axis, False)

                    self.ui.current_values = self.ui.text_widget.get(1.0, END).split()
                    new_values = self.ui.current_values[self.ui.shift_count:]
                    self.ui.current_values = new_values
                    self.map_data = self.ui.current_values[start_index:end_index]
                    mode3d.paste_data(True, self.map_data, self.row, self.col, True)
                    if not (start_index - (self.col + self.row) < 0):
                        self.x_axis = self.ui.current_values[start_index - self.col:start_index]
                        self.y_axis = self.ui.current_values[start_index - (self.col + self.row):start_index - self.col]
                        mode3d.paste_x_data(True, self.x_axis, True)
                        mode3d.paste_y_data(True, self.y_axis, True)

                    mode3d.check_all()

                    break

    def highlight_text_map(self, start_index, end_index):
        self.ui.text_widget.tag_remove(f"{self.map_name}", 1.0, END)
        self.ui.text_widget.tag_configure(f"{self.map_name}", background="#555")

        start_index += self.ui.shift_count
        end_index += self.ui.shift_count

        end_index -= 1

        start_row = start_index // self.ui.columns
        start_col = start_index % self.ui.columns

        end_row = end_index // self.ui.columns
        end_col = end_index % self.ui.columns

        start = f"{start_row + 1}.{start_col * 6}"
        end = f"{end_row + 1}.{(end_col + 1) * 6 - 1}"

        self.ui.text_widget.tag_add(f"{self.map_name}", start, end)
        self.ui.text_widget.see(start)

    def highlight_2d_map(self, start_index, end_index):
        start_index += self.ui.shift_count
        end_index += self.ui.shift_count

        self.ui.start_index_maps.append(start_index)
        self.ui.end_index_maps.append(end_index)

        from Module_2D import Mode2D
        mode2d = Mode2D(self.ui)
        mode2d.draw_canvas(self.ui)

    def write_map(self):
        map_values = []

        if not self.double_click:
            return

        for yi, entry in enumerate(self.ui.entry_y_widgets):
            map_values.append(entry.get())

        for xi, entry in enumerate(self.ui.entry_x_widgets[0]):
            map_values.append(entry.get())

        index_map = 0

        for i in range(self.ui.rows_3d):
            for j in range(self.ui.columns_3d):
                index_map += 1
                map_values.append(self.ui.entry_widgets[i][j].get())

        self.ui.current_values = self.ui.text_widget.get(1.0, END).split()

        with open(self.file_path, 'r') as file:
            content = file.read().split('\n')
            index = self.last_map_index * 4
            start = int(content[index + 1]) + self.ui.shift_count
            end = int(content[index + 2]) + self.ui.shift_count

        index = 0

        for i in range(start - (xi + 1 + yi + 1), end):
            self.ui.current_values[i] = map_values[index]
            index += 1

        self.ui.text_widget.delete(1.0, END)

        rows = [self.ui.current_values[i:i + self.ui.columns] for i in range(0, len(self.ui.current_values), self.ui.columns)]

        for row in rows:
            formatted = ' '.join(f"{value:05}" for value in row)
            self.ui.text_widget.insert(END, formatted + '\n')

        self.reapply_highlight_text()

        from Module_2D import Mode2D
        from Utilities import Utility
        mode2d = Mode2D(self.ui)
        utility = Utility(self.ui)
        mode2d.update_2d(self.ui)
        int_values = [int(x) for x in self.ui.current_values]
        utility.check_difference_values(int_values, True, self.ui)

    def reapply_highlight_text(self):
        if not os.path.exists(self.file_path):
            return
        tags = self.ui.text_widget.tag_names()
        for tag in tags:
            self.ui.text_widget.tag_delete(tag)
        with open(self.file_path, 'r') as file:
            content = file.read().split('\n')
            for i in range(0, len(content), 4):
                map_name = content[i]
                start_index = int(content[i + 1]) + self.ui.shift_count
                end_index = int(content[i + 2]) + self.ui.shift_count

                self.ui.text_widget.tag_configure(f"{map_name}", background="#555")

                end_index -= 1

                start_row = start_index // self.ui.columns
                start_col = start_index % self.ui.columns

                end_row = end_index // self.ui.columns
                end_col = end_index % self.ui.columns

                start = f"{start_row + 1}.{start_col * 6}"
                end = f"{end_row + 1}.{(end_col + 1) * 6 - 1}"

                self.ui.text_widget.tag_add(f"{map_name}", start, end)

    def remove_item(self):
        selected_index = self.ui.map_list.curselection()

        if selected_index:
            index = selected_index[0]
            if self.last_map_index == index:
                from Module_3D import Mode3D
                mode3d = Mode3D(self.ui)
                mode3d.set_default()
            item = self.ui.map_list.get(index)
            with open(self.file_path, 'r') as file:
                content = file.read().split("\n")
                for i in range(len(content)):
                    if content[i] == item:
                        del content[i:i + 4]
                        break
            with open(self.file_path, 'w') as file:
                for i in range(len(content)):
                    file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])
            self.ui.map_list_counter -= 1
            self.reapply_highlight_text()
            self.ui.map_list.delete(selected_index)

    def show_context_menu(self, event):
        selected_index = self.ui.map_list.curselection()
        if selected_index:
            self.ui.remove_menu.post(event.x_root, event.y_root)

    def hide_context_menu(self, event):
        self.ui.remove_menu.unpost()

    def import_map(self):
        result = subprocess.run(['zenity', '--file-selection'], capture_output=True, text=True)

        if result.returncode == 0:
            file_path = result.stdout.strip()
        else:
            return

        if file_path:
            self.ui.map_list_counter = 0
            self.last_map_index = 0
            from Module_3D import Mode3D
            mode3d = Mode3D(self.ui)
            mode3d.set_default()
            with open(file_path, 'r') as file:
                content = file.read().split('\n')
                if len(content) % 4 == 0:
                    with open(self.file_path, 'w') as temp_file:
                        for i in range(len(content)):
                            temp_file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])
                        self.ui.map_list.delete(0, END)
                        self.ui.maps_names = []
                        self.first_run = False
                    for i in range(len(content) // 4):
                        self.map_name = content[i * 4]
                        self.start_index = int(content[(i * 4) + 1])
                        self.end_index = int(content[(i * 4) + 2])
                        self.size = content[(i * 4) + 3]
                        self.ui.map_list.insert(self.ui.map_list_counter, self.map_name)
                        self.ui.maps_names.append(self.map_name)
                        self.highlight_text_map(self.start_index, self.end_index)
                        self.highlight_2d_map(self.start_index, self.end_index)
                        self.ui.map_list_counter += 1
                    self.reapply_highlight_text()
                else:
                    messagebox.showerror("Error", "Please select a valid file!")
                    return

    def export_map(self):
        if self.file_path == "":
            messagebox.showerror("Error", "You have to create or import a mappack before you can export it!")
            return

        file_path = self.linux_asksaveasfilename(initial_dir="", defaultextension=".mp", filetypes=[("Mappack Files", "*.mp")],
                                                 initialfile="")

        with open(self.file_path, 'r') as ori:
            content = ori.read().split('\n')

        with open(file_path, 'w') as file:
            for i in range(len(content)):
                file.write(f"{content[i]}\n" if i < len(content) - 1 else content[i])

    def linux_asksaveasfilename(self, initial_dir="", defaultextension=".mp", filetypes=[("Mappack Files", "*.mp")],
                                initialfile=""):
        try:
            filter_string = ' '.join([f'--file-filter={ftype[0]} | {ftype[1]}' for ftype in filetypes])

            command = ['zenity', '--file-selection', '--save', '--confirm-overwrite',
                       '--filename=' + initialfile, '--file-filter=*.mp']

            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                file_path = result.stdout.strip()
                if not file_path.endswith(defaultextension):
                    file_path += defaultextension
                return file_path
            else:
                return

        except FileNotFoundError:
            messagebox.showerror("Error", "You don't have zenity installed!")