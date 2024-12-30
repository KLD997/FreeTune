from tkinter import *
from tkinter import messagebox

class Value_Dialog_3D:
    def __init__(self, ui):
        self.ui = ui

    def value_dialog(self):
        self.value_dialog_window = Toplevel(bg="#333")

        screen_width = self.ui.window.winfo_screenwidth()
        screen_height = self.ui.window.winfo_screenheight()

        width = 250
        height = 125
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.value_dialog_window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.value_dialog_window.title("Value Changer")

        self.selected_value = ""

        self.entry = Entry(self.value_dialog_window, bg="#555", fg="white", highlightthickness=0, font=('Arial', 11))
        self.entry.grid(row=0, column=0, columnspan=3, padx=40, pady=10)

        button1 = Button(self.value_dialog_window, text="=", font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", command=lambda: self.change_value("="))
        button2 = Button(self.value_dialog_window, text="+", font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", command=lambda: self.change_value("+"))
        button3 = Button(self.value_dialog_window, text="%", font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", command=lambda: self.change_value("%"))

        button1.grid(row=1, column=0, padx=10, pady=5)
        button2.grid(row=1, column=1, padx=10, pady=5)
        button3.grid(row=1, column=2, padx=10, pady=5)

        ok_button = Button(self.value_dialog_window, text="Ok", command=self.calculate, font=('Arial', 11), bg="#444", highlightthickness=0, fg="white", width=6)
        ok_button.grid(row=2, column=0, columnspan=3, pady=10)
        self.entry.focus_set()

    def change_value(self, value):
        self.selected_value = value

    def calculate(self):
        if not self.selected_value:
            entry_message = ""
            if self.entry.get() == "":
                entry_message += "and enter a value in entry box"
            messagebox.showerror("Error", f"Please select an operation {entry_message}!")
            return
        if self.entry.get() == "":
            messagebox.showerror("Error", "Please enter a value in entry box!")
            return

        try:
            int_value = int(self.entry.get())
            if 0 > int_value or int_value > 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        from Module_3D import Mode3D
        mode3d = Mode3D(self.ui)

        if self.selected_value == "=":
            mode3d.set_text(int_value)
        if self.selected_value == "+":
            mode3d.increase_selected_text(int_value)
        if self.selected_value == "%":
            mode3d.increase_selected_text_per(int_value)