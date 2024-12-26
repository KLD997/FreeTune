import tkinter
from tkinter import *
from tkinter import messagebox
import math

class TextAddons:
    def __init__(self, ui):
        self.ui = ui
        self.entry_widget = Entry()

    def edit_mode(self, event):
        self.ui.edit_mode_active = True
        if self.ui.text_widget.tag_ranges(SEL):
            sel_start = self.ui.text_widget.index(SEL_FIRST)
            sel_end = self.ui.text_widget.index(SEL_LAST)
            selected_text = self.ui.text_widget.get(sel_start, sel_end).strip()

            if len(selected_text) == 5:
                place_info = self.ui.text_widget.bbox(SEL_FIRST)
                x, y, width, height = place_info
                x_root = x
                y_root = y
                self.create_entry(sel_start, sel_end, selected_text, x_root, y_root)

        return "break"

    def create_entry(self, start_index, end_index, text, x_root, y_root):
        if self.entry_widget:
            self.entry_widget.destroy()

        self.entry_widget = Entry(self.ui.window, bg="#555", fg="white", highlightthickness=0, bd=0, font=("Courier", 9))
        self.entry_widget.insert(0, text)
        self.entry_widget.place(x=x_root + 14, y=y_root + 37, width=40, height=13)

        self.entry_widget.focus_set()
        self.entry_widget.bind("<Return>", lambda e: self.save_edit(e, start_index, end_index))
        self.ui.window.bind("<Button-1>", lambda event: self.on_outside_click(event, self.entry_widget, start_index, end_index))

    def on_outside_click(self, event, widget, func2, func3):
        if self.ui.edit_mode_active:
            if widget.winfo_exists() and widget is not None:
                try:
                    x1, y1, x2, y2 = widget.bbox("all")
                    if not (x1 <= event.x <= x2 and y1 <= event.y <= y2):
                        self.save_edit(event, func2, func3)
                except tkinter.TclError:
                    return

    def save_edit(self, event, start_index=None, end_index=None):
        if self.entry_widget:
            new_text = self.entry_widget.get().strip()
            try:
                int(new_text)
            except ValueError:
                self.entry_widget.destroy()
                self.ui.text_widget.tag_remove(SEL, 1.0, END)
                messagebox.showerror("Invalid Number!", "You have entered an invalid number!")
                return
            if len(new_text) <= 5:
                new_text = f"{new_text:05}"
                self.ui.text_widget.delete(start_index, end_index)
                self.ui.text_widget.insert(start_index, new_text)

            self.entry_widget.destroy()
            self.entry_widget = None
            from Utilites import Utility
            self.utility = Utility(self)
            self.utility.check_value_changes(self.ui)
            self.ui.edit_mode_active = False

    def start_selection(self, event):
        self.selection_start = self.ui.text_widget.index(f"@{event.x},{event.y}")

    def stop_drag(self, event):
        end_str = str(self.ui.text_widget.index(f"@{event.x},{event.y}"))
        start_str = str(self.selection_start)
        end = int(end_str.split('.')[1])
        self.end_row = int(end_str.split('.')[0])
        self.start_row = int(start_str.split('.')[0])
        start = int(start_str.split('.')[1])

        end_temp = end / 6
        start_temp = start / 6

        temp1 = math.ceil(end_temp)
        temp2 = math.floor(start_temp)

        self.end = (temp1 * 6) - 1
        self.start = (temp2 * 6)

        self.on_enter()
        self.adjust_selection()

    def adjust_selection(self):
        try:
            sel_start = self.ui.text_widget.index(SEL_FIRST)
            sel_end = self.ui.text_widget.index(SEL_LAST)
            selected_text = self.ui.text_widget.get(sel_start, sel_end)
        except tkinter.TclError:
            return

        row, col = sel_end.split('.')
        col = int(col)

        if selected_text.endswith(' '):
            col -= 1

        self.ui.text_widget.mark_set(INSERT, f"{row}.{col}")

        self.ui.text_widget.tag_remove(SEL, "1.0", END)
        self.ui.text_widget.tag_add(SEL, f"{sel_start}", f"{row}.{col}")

    def on_enter(self):
        self.ui.text_widget.tag_remove(SEL, "1.0", END)
        self.ui.text_widget.tag_add(SEL, f"{self.start_row}.{self.start}", f"{self.end_row}.{self.end}")

    def disable_double_click_selection(self, event):
        return 'break'

    def disable_user_input(self, event):
        return "break"

    def update_selected_count(self, event):
        if self.ui.text_widget.tag_ranges("sel"):
            selected_text = self.ui.text_widget.get("sel.first", "sel.last")
        else:
            selected_text = ""
        self.ui.selected_count = len(selected_text.split())
        self.ui.selected_count_label.configure(text=f"Selected: {self.ui.selected_count}")