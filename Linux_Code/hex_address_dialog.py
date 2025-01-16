from tkinter import *
from tkinter import messagebox
from customtkinter import *

class HexAddressDialog:
    def __init__(self, ui):
        self.ui = ui

    def hex_find_dialog(self):
        dialog_find = Toplevel(bg="#333")
        self.dialog_find = dialog_find
        dialog_find.resizable(False, False)
        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()
        width = 180
        height = 120
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        dialog_find.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        dialog_find.title("Find Hex Address")
        label = CTkLabel(dialog_find, text="Enter a hex address:", fg_color="#333", text_color="white", font=("Roboto", 15))
        label.pack(pady=5)
        self.find_entry = CTkEntry(dialog_find, fg_color="#555", text_color="white", width=120)
        self.find_entry.pack(pady=5)
        button_find = CTkButton(dialog_find, text="Find", command=self.find, fg_color="#444", text_color="white", hover_color="#555", width=60)
        button_find.pack(pady=5, padx=5)

    def find(self):
        try:
            index = int(self.find_entry.get(), 16)
            if not index % 2 == 0:
                raise ValueError
            index = index // 2
            if index < 0 or index > len(self.ui.unpacked):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid hex address!")
            self.find_entry.focus_set()
            return

        self.ui.highlight_start = index
        self.highlight_hex(index)
        self.dialog_find.destroy()


    def highlight_hex(self, index):
        self.ui.text_widget.tag_remove("highlight", 1.0, END)
        self.ui.text_widget.tag_configure("highlight", background="#907900")

        row = index // self.ui.columns
        col = index % self.ui.columns

        start = f"{row + 1}.{col * 6}"
        end = f"{row + 1}.{(col + 1) * 6 - 1}"

        self.ui.text_widget.tag_add("highlight", start, end)
        self.ui.text_widget.see(start)

        frame = self.ui.num_rows * self.ui.columns
        frames_num = index // frame
        self.ui.current_frame = frames_num * frame

        if self.ui.current_frame > 0:
            self.ui.red_line = int(index) - self.ui.current_frame
        else:
            self.ui.red_line = int(index)

        value = self.ui.current_values[index]

        self.ui.text_value.configure(text=f"Value: {value:05}")

        from Module_2D import Mode2D
        mode2d = Mode2D(self.ui)

        mode2d.draw_canvas(self.ui)