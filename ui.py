from time import sleep
from tkinter import *
from tkinter import ttk
from customtkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LinOLS:
    def __init__(self, window):
        from text_view import TextView
        from Module_2D import Mode2D
        from Utilites import Utility
        from find_dialog import Find_Dialog
        from File_Import import FileImport
        from difference_dialog import DifferenceDialog
        from value_dialog import ValueDialog
        from text_addons import TextAddons
        self.window = window
        window.title("LinOLS")

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.width = 1500
        window.height = 600

        x = (screen_width / 2) - (window.width / 2)
        y = (screen_height / 2) - (window.height / 2)
        window.geometry(f"{window.width}x{window.height}+{int(x)}+{int(y)}")

        self.text_view_ = TextView(self)
        self.mode2d = Mode2D(self)
        self.utility = Utility(self)
        self.find_dialog = Find_Dialog(self)
        self.file_import = FileImport(self)
        self.diff_dialog = DifferenceDialog(self)
        self.value_dial = ValueDialog(self)
        self.text_addons = TextAddons(self)

        self.file_path = ""
        self.columns = 20
        self.num_rows = 55
        self.unpacked = []
        self.current_frame = 0
        self.x = 0
        self.percentage_num = 0
        self.total_rows = 0
        self.low_high = True
        self.open = False
        self.import_allow = False
        self.current_values = []
        self.found_values = []
        self.found_values_counter = 0
        self.new_path = ""
        self.imported_values = []
        self.differences = []
        self.differences_color = []
        self.ori_values = []
        self.index_differences = []
        self.start_time = 0
        self.running = True
        self.hold_time = 0.5
        self.new_values = []
        self.selected_count = 0
        self.values = []
        self.shift_count = 0
        self.end_time = 0
        self.edit_mode_active = False
        self.display_sel = False
        self.sel_start = 0
        self.sel_end = 0
        self.highlight_start = None
        self.return_text = False
        self.red_line = None
        self.difference_index = -1

        window.config(bg="#333")

        window.option_add("*Font", "Nimbus_Sans 9")

        self.notebook = ttk.Notebook(window)
        style = ttk.Style()
        style.configure("TNotebook", background="#333")
        style.configure("TNotebook.Tab", background="#333", foreground="white")
        style.map("TNotebook.Tab", background=[('selected', '#555')])
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.setup_ui()

    def setup_ui(self):
        tab1 = Frame(self.notebook, bg="#333")
        self.notebook.add(tab1, text=" Text ")

        text_frame = Frame(tab1, bg="#333")
        text_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)

        self.text_widget = Text(text_frame, bg="#333333", bd=0, highlightthickness=0, fg="white", font=("Courier", 9))
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=True)
        self.text_widget.configure(insertbackground='white', undo=True)

        self.scroll_bar = Scrollbar(text_frame, command=self.text_widget.yview, bg="#333")
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        buttons_frame = CTkFrame(tab1, fg_color="#333")
        buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        center_frame_left = CTkFrame(tab1, fg_color="#333")
        center_frame_left.grid(row=1, column=0, pady=5)

        center_frame = CTkFrame(tab1, fg_color="#333")
        center_frame.grid(row=1, column=0, pady=5)

        dec16_low_high = CTkButton(buttons_frame, text="16-bit Lo-Hi", width=6, hover_color="#555", fg_color="#444", text_color="white", command=lambda: self.text_view_.change_display_mode("low_high"))
        dec16_low_high.grid(row=0, column=0, padx=5, sticky="w")

        dec16_high_low = CTkButton(buttons_frame, text="16-bit Hi-Lo", width=6, hover_color="#555", fg_color="#444", text_color="white", command=lambda: self.text_view_.change_display_mode("high_low"))
        dec16_high_low.grid(row=0, column=1, padx=5)

        self.selected_count_label = CTkButton(center_frame_left, text="Selected: 0", width=100, hover_color="#555", fg_color="#444", text_color="white")
        self.selected_count_label.grid(row=0, column=0, padx=198)

        button_2d = CTkButton(center_frame_left, text="Text to 2D", hover_color="#555",width=100, command=lambda: self.mode2d.text_to_2d(self), fg_color="#444", text_color="white")
        button_2d.grid(row=0, column=1, padx=200)


        '''COLUMNS FRAME'''
        columns_frame = CTkFrame(center_frame, border_color="#555", border_width=1, fg_color="#333")
        columns_frame.grid(row=0, column=0, padx=5)

        label_col = CTkLabel(columns_frame, text="Col:", width=3, height=2, fg_color="#333", text_color="white")
        label_col.grid(row=0, column=0, padx=5, pady=3)

        self.entry = CTkEntry(columns_frame, fg_color="#555", text_color="white", width=28)
        self.entry.grid(row=0, column=1, padx=5, pady=3)
        self.entry.insert(END, str(self.columns))

        apply_columns = CTkButton(columns_frame, text="Apply", width=6, hover_color="#555", command=lambda: self.utility.adjust_columns(self), fg_color="#444", text_color="white")
        apply_columns.grid(row=0, column=2, padx=5, pady=3)

        '''SHIFT FRAME'''
        shift_frame = CTkFrame(center_frame, border_color="#555", border_width=1, fg_color="#333")
        shift_frame.grid(row=0, column=1, padx=5)

        label_shift = CTkLabel(shift_frame, text="Shift:", width=3, height=2, fg_color="#333", text_color="white")
        label_shift.grid(row=0, column=0, padx=5, pady=3)

        self.entry_position = CTkEntry(shift_frame, fg_color="#555", text_color="white", width=28)
        self.entry_position.grid(row=0, column=1, padx=5, pady=3)
        self.entry_position.insert(0, "00")

        apply_position = CTkButton(shift_frame, text="Apply", width=6, hover_color="#555", fg_color="#444", text_color="white", command=lambda: self.utility.move_items(self))
        apply_position.grid(row=0, column=2, padx=5, pady=3)

        '''EDIT BUTTONS'''
        edit_buttons = CTkFrame(tab1, fg_color="#333")
        edit_buttons.grid(row=1, column=0, padx=5, pady=5, sticky=E)

        copy_button = CTkButton(edit_buttons, text="Copy", hover_color="#555", width=6, command=self.utility.copy_values,  fg_color="#444", text_color="white")
        copy_button.grid(row=0, column=1, padx=5, sticky=E)

        paste_button = CTkButton(edit_buttons, text="Paste", hover_color="#555", width=6, command=lambda: self.utility.paste_values(self), fg_color="#444", text_color="white")
        paste_button.grid(row=0, column=2, padx=5, sticky=E)

        undo = CTkButton(edit_buttons, text="Undo", hover_color="#555", width=6, command=self.utility.undo, fg_color="#444", text_color="white")
        undo.grid(row=0, column=3, padx=5, sticky=E)

        redo = CTkButton(edit_buttons, text="Redo", hover_color="#555", width=6, command=self.utility.redo, fg_color="#444", text_color="white")
        redo.grid(row=0, column=4, padx=5, sticky=E)

        self.text_widget.config(yscrollcommand=self.scroll_bar.set)

        tab2 = CTkFrame(self.notebook, fg_color="#333")
        self.notebook.add(tab2, text=" 2D ")

        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)

        self.fig.patch.set_facecolor('#333')
        self.ax.set_facecolor('#333')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=tab2)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, padx=0, pady=0, sticky='nsew')

        self.canvas.get_tk_widget().config(highlightthickness=0)

        self.canvas.mpl_connect("button_press_event", self.mode2d.on_canvas_click)

        tab2.grid_rowconfigure(0, weight=1)
        tab2.grid_columnconfigure(0, weight=1)

        navigation_buttons_frame = CTkFrame(tab2, fg_color="#333")
        navigation_buttons_frame.grid(row=1, column=0, columnspan=6, pady=5, sticky=W)

        update_frame = CTkFrame(tab2, fg_color="#333")
        update_frame.grid(row=1, column=0, padx=5)

        center_frame_2d_spacing = CTkFrame(tab2, fg_color="#333")
        center_frame_2d_spacing.grid(row=1, column=0, padx=5, pady=5)

        center_frame_2d = CTkFrame(tab2, fg_color="#333")
        center_frame_2d.grid(row=1, column=0, padx=5, pady=5)

        right_frame_2d = CTkFrame(tab2, fg_color="#333")
        right_frame_2d.grid(row=1, column=0, padx=5, pady=5, sticky=E)

        prev_button = CTkButton(navigation_buttons_frame, text="<", hover_color="#555", width=60, command=self.mode2d.prev_page, fg_color="#444", text_color="white")
        prev_button.grid(row=0, column=0, padx=5)

        fast_backwards_button = CTkButton(navigation_buttons_frame, text="<<", hover_color="#555", width=60, command=lambda: self.mode2d.fast_movement("left"), fg_color="#444", text_color="white")
        fast_backwards_button.grid(row=0, column=1, padx=5)

        next_button = CTkButton(right_frame_2d, text=">", hover_color="#555", width=60, command=self.mode2d.next_page, fg_color="#444", text_color="white")
        next_button.grid(row=0, column=1, padx=5)

        fast_forward_button = CTkButton(right_frame_2d, text=">>", hover_color="#555", width=60, command=lambda: self.mode2d.fast_movement("right"), fg_color="#444", text_color="white")
        fast_forward_button.grid(row=0, column=0, padx=5)

        load_and_update_button = CTkButton(update_frame, text="Update", hover_color="#555", width=100, command=lambda: self.mode2d.update_2d(self), fg_color="#444", text_color="white")
        load_and_update_button.grid(row=0, column=0, padx=148)

        self.text_value = CTkButton(update_frame, text="Value: 00000", hover_color="#555", width=100, fg_color="#444", text_color="white")
        self.text_value.grid(row=0, column=2, padx=150)

        update_percentage = CTkButton(center_frame_2d_spacing, text="%", hover_color="#555", width=6, command=lambda: self.mode2d.percentage(True, "set"), fg_color="#444", text_color="white")
        update_percentage.grid(row=0, column=0, padx=58)

        update_percentage_1 = CTkButton(center_frame_2d_spacing, text="%", hover_color="#555", width=6, command=lambda: self.mode2d.percentage(True, "set"), fg_color="#444", text_color="white")
        update_percentage_1.grid(row=0, column=1, padx=60)

        percent_minus = CTkButton(center_frame_2d, text="-", width=3, hover_color="#555", command=lambda: self.mode2d.percentage(False, "minus"), fg_color="#444", text_color="white")
        percent_minus.grid(row=0, column=0, padx=5)

        self.percentage_entry = CTkEntry(center_frame_2d, width=28, fg_color="#555", text_color="white")
        self.percentage_entry.grid(row=0, column=1, padx=5)
        self.percentage_entry.insert(END, "00")

        percent_plus = CTkButton(center_frame_2d, text="+", width=3, hover_color="#555", command=lambda: self.mode2d.percentage(False, "plus"), fg_color="#444", text_color="white")
        percent_plus.grid(row=0, column=2, padx=5)

        tab1.grid_rowconfigure(0, weight=1)
        tab1.grid_columnconfigure(0, weight=1)

        menu_bar = Menu(self.window, bg="#333", fg="white")
        self.window.config(menu=menu_bar)
        file_menu = Menu(menu_bar, tearoff=0, bg="#333", fg="white")
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=lambda: self.text_view_.open_file(self))
        file_menu.add_command(label="Save", command=self.text_view_.save_file)

        options_menu = Menu(menu_bar, tearoff=0, bg="#333", fg="white")
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Find", command=self.find_dialog.find_dialog)
        options_menu.add_command(label="Import", command=lambda: self.file_import.import_file(self))
        options_menu.add_command(label="Difference", command=lambda: self.diff_dialog.differences_dialog(self))
        options_menu.add_command(label="Value Changer", command=lambda event=None: self.value_dial.value_dialog(self, event))

        self.text_widget.bind("<Button-1>", self.text_addons.start_selection)
        self.text_widget.bind("<ButtonRelease-1>", self.text_addons.stop_drag)
        self.text_widget.bind("<Double-1>", self.text_addons.disable_double_click_selection)
        self.text_widget.bind("<Key>", self.text_addons.disable_user_input)
        self.text_widget.bind("<percent>", lambda event=None: self.value_dial.value_dialog(self, event))
        self.text_widget.bind("<e>", self.text_addons.edit_mode)
        self.text_widget.bind("<E>", self.text_addons.edit_mode)

        self.text_widget.bind('<Motion>', self.text_addons.update_selected_count)

        self.window.protocol("WM_DELETE_WINDOW", self.exit_app)

    def exit_app(self, event=None):
        if self.new_path and os.path.exists(self.new_path):
            os.remove(self.new_path)
        self.window.quit()