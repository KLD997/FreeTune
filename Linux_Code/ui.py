import time

from PyQt6.QtCore import QAbstractTableModel, QModelIndex
from PyQt6.QtWidgets import QMainWindow, QWidget, QTabWidget, QTableView, QHeaderView, QGridLayout, QPushButton, QFrame, \
    QLabel, QLineEdit, QSizePolicy, QSpacerItem, QTableWidget, QListWidget, QVBoxLayout, QMenu, QMessageBox
from PyQt6.QtGui import QAction, QGuiApplication, QColor, QKeyEvent, QKeySequence, QShortcut, QFont, QPalette, QIcon
from PyQt6.QtCore import Qt, QPoint
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import os

class LinOLS(QMainWindow):
    def __init__(self):
        super().__init__()

        from text_view import TextView
        from Module_2D import Mode2D
        from text_addons import TextAddons
        from Module_3D import Mode3D
        from maps import Maps_Utility
        from potential_maps.potential_maps import Potential_maps_manager
        from custom_dialogs.dialog_handler import DialogManager
        from canva_3d.canva_3d_window import TkWindowManager

        self.setWindowTitle("LinOLS")

        self.setMinimumWidth(1300)

        screen = QGuiApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()

        window_width = 1500
        window_height = 600

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.setGeometry(x, y, window_width, window_height)

        self.text_view_ = TextView(self)
        self.mode2d = Mode2D(self)
        self.text_addons = TextAddons(self)
        self.mode3d = Mode3D(self)
        self.maps = Maps_Utility(self)
        self.potential_maps_manager = Potential_maps_manager(self)
        self.dialog_manager = DialogManager(self)
        self.tk_win_manager = TkWindowManager(self)

        '''General variables'''
        self.file_path = "" # file path of the loaded file
        self.columns = 20 # num of columns
        self.num_rows = 55 # num of rows for 2d
        self.unpacked = [] # all original numbers
        self.low_high = True  # low_high or high_low
        self.current_values = []  # current values in text and 2d view

        '''Text view variables'''
        self.return_text = False # used for returning to previous value
        self.tab1_selected = True # true when tab1 is selected

        '''2d variables'''
        self.current_frame = 0 # current 2d frame
        self.percentage_num = 0 # percentage number in 2d
        self.display_sel = False # flag to control whether selection should be displayed in 2d
        self.sel_start = 0 # start of the selection
        self.sel_end = 0 # end of selection
        self.red_line = None  # a red line in 2d
        self.num_rows = 55 # number of rows displayed in 2d
        self.sync_2d_scroll = False # sync 2d to text

        '''Find dialog variables'''
        self.found_valuesx_values = [] # all found values
        self.found_values_counter = 0 # how many values where found

        '''Difference dialog variables'''
        self.differences = [] # all differences
        self.differences_color = [] # color of all differences
        self.ori_values = [] # all ori values for differences
        self.index_differences = [] # indexes of all differences

        '''Shift variables'''
        self.start_time = 0 # start time for shifting values
        self.values = [] # values for shift in text view
        self.shift_count = 0 # count of shift
        self.end_time = 0 # end time for shifting

        '''Maps variables'''
        self.map_list_counter = 0  # number of maps
        self.start_index_maps = []  # start indexes for created/imported maps
        self.end_index_maps = []  # end indexes for created/imported maps
        self.maps_names = []  # all map names for created/imported maps
        self.signed_values = False  # 3d signed values
        self.map_decimal = False  # do map values in 3d have decimal numbers
        self.x_axis_decimal = False  # do x-axis values have a decimal numbers
        self.y_axis_decimal = False  # do y-axis values have a decimal numbers

        '''3D variables'''
        self.num_rows_3d = 15
        self.num_columns_3d = 20
        self.column_width_3d = 55
        self.map_opened = False

        self.original = []
        self.original_x = []
        self.original_y = []

        for i in range(self.num_rows_3d):
            row = []
            self.original_y.append(i + 1)
            for x in range(self.num_columns_3d):
                row.append(0)
            self.original.append(row)

        for i in range(self.num_columns_3d):
            self.original_x.append(i + 1)

        self.x_values = []  # current 3d x-axis values
        self.y_values = []  # current 3d y-axis values
        self.map_values = []  # current 3d map values

        self.new_width = 0  # new width of entry boxes in 3d

        self.focused_3d_tab = False

        '''Potential maps variables'''
        self.potential_maps_start = [] # all potential maps start indexes
        self.potential_maps_end = [] # all potential maps end indexes
        self.potential_maps_names = [] # all potential maps names

        self.potential_map_added = False # for checking if potential map has been added successfully
        self.potential_map_index = None

        '''Custom Dialogs'''
        self.dialog_terminate = True

        self.setStyleSheet("background-color: #333;")

        self.setup_ui()

    def setup_ui(self):
        self.create_menu_bar()

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.tabs.currentChanged.connect(self.text_addons.on_tab_changed)

        self.tab1 = QWidget()
        self.tab1.setStyleSheet("border: 0;")
        self.tab2 = QWidget()
        self.tab2.setStyleSheet("border: 0;")
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.tabs.addTab(self.tab1, "Text")
        self.tabs.addTab(self.tab2, "2D")
        self.tabs.addTab(self.tab3, "3D")
        self.tabs.addTab(self.tab4, "Maps")

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.setup_tab4()

        self.create_shortcut(self.tab1, "Ctrl+F")
        self.create_shortcut(self.tab2, "Ctrl+F")

        self.create_shortcut(self.tab1, "Ctrl+G")
        self.create_shortcut(self.tab2, "Ctrl+G")

        self.create_shortcut(self.tab1, "Shift+5")

        self.create_shortcut(self.tab1, "w")
        self.create_shortcut(self.tab1, "m")

        self.create_shortcut(self.tab1, "k")

        self.clean_up()

    def create_shortcut(self, tab, key_sequence):
        shortcut = QShortcut(QKeySequence(key_sequence), tab)
        shortcut.activated.connect(lambda: self.on_shortcut_activated(key_sequence))

    def on_shortcut_activated(self, key_sequence):
        if key_sequence == "Ctrl+F":
            self.text_addons.open_find_dialog()
        elif key_sequence == "Ctrl+G":
            self.text_addons.open_hex_address_dialog()
        elif key_sequence == "Shift+5":
            self.text_addons.open_value_dialog()
        elif key_sequence == "w":
            self.text_addons.adjust_columns("-")
        elif key_sequence == "m":
            self.text_addons.adjust_columns("+")
        elif key_sequence == "k":
            self.maps.add_map()

    def setup_tab1(self):
        main_layout = QGridLayout()

        self.table_view = CustomTableView(self)
        main_layout.addWidget(self.table_view, 0, 0)

        font = QFont("Cantarell", 11)
        self.table_view.setFont(font)

        self.table_view.setStyleSheet("""
            QTableView {
                background-color: #333;
            }
            QTableView::item:selected {
                background-color: #5b9bf8;
                color: white;
            }
            QHeaderView::section {
                background-color: #363636;
                color: white;
            } 
        """)

        self.model = QTableModel(self.unpacked, self)
        self.table_view.setModel(self.model)

        self.table_view.horizontalHeader().setVisible(False)

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.table_view.verticalHeader().setFixedWidth(60) # change width of x-axis

        left_grid_layout = QGridLayout()

        left_grid_layout.setContentsMargins(0, 0, 0, 0)
        left_grid_layout.setHorizontalSpacing(10)
        left_grid_layout.setVerticalSpacing(10)

        mid_grid_layout = QGridLayout()

        mid_grid_layout.setSpacing(0)

        mid_grid_layout.setContentsMargins(0, 0, 0, 0)
        mid_grid_layout.setHorizontalSpacing(0)
        mid_grid_layout.setVerticalSpacing(10)

        right_grid_layout = QGridLayout()

        right_grid_layout.setContentsMargins(0, 0, 0, 0)
        right_grid_layout.setHorizontalSpacing(10)
        right_grid_layout.setVerticalSpacing(10)

        button_style = """
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 65px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        QPushButton:disabled {
            background-color: #555;
            color: #aaa;
        }
        """

        self.btn_lo_hi = QPushButton("16-bit Lo-Hi", self)
        self.btn_lo_hi.clicked.connect(lambda: self.text_view_.ask_change_display_mode("low_high"))
        self.btn_lo_hi.setStyleSheet(button_style)

        self.btn_hi_lo = QPushButton("16-bit Hi-Lo", self)
        self.btn_hi_lo.clicked.connect(lambda: self.text_view_.ask_change_display_mode("high_low"))
        self.btn_hi_lo.setStyleSheet(button_style)

        btn2 = QPushButton("Add Map", self)
        btn2.setStyleSheet(button_style)
        btn2.clicked.connect(self.maps.add_map)

        btn3 = QPushButton("Text to 2D", self)
        btn3.setStyleSheet(button_style)
        btn3.clicked.connect(lambda: self.mode2d.text_to_2d(self))

        self.sel_btn = QPushButton("Selected: 0", self)
        self.sel_btn.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 65px;
            margin-right: 10px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """)

        frame_col = QFrame(self)
        frame_col.setFrameShape(QFrame.Shape.StyledPanel)
        frame_col.setFrameShadow(QFrame.Shadow.Raised)
        frame_col.setStyleSheet("""
            border: 2px solid #888;
            border-radius: 5px;
        """)

        frame_col.setFixedHeight(35)
        frame_col.setFixedWidth(140)

        label_col = QLabel("Width:", self)
        label_col.setStyleSheet("""
            border: 0;
            color: white;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background: transparent;
            margin-left: 5px;
        """)

        self.entry_col = QLineEdit(f"{self.columns:02}", self)
        self.entry_col.setStyleSheet("""
            border: 2px;
            border-radius: 5px;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background-color: #555;
            height: 25px;
            width: 28px;
            margin-left: 50px;                    
        """)

        self.entry_col.setReadOnly(True)

        self.entry_col.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.entry_col.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_col_plus = QPushButton("+", self)
        btn_col_plus.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 10px;
            margin-left: 8px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """)
        btn_col_plus.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_col_plus.clicked.connect(lambda: self.text_addons.adjust_columns("+"))

        btn_col_minus = QPushButton("-", self)
        btn_col_minus.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 10px;
            margin-left: 5px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """)
        btn_col_minus.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_col_minus.clicked.connect(lambda: self.text_addons.adjust_columns("-"))

        frame_shift = QFrame(self)
        frame_shift.setFrameShape(QFrame.Shape.StyledPanel)
        frame_shift.setFrameShadow(QFrame.Shadow.Raised)
        frame_shift.setStyleSheet("""
            border: 2px solid #888;
            border-radius: 5px;
        """)

        frame_shift.setFixedHeight(35)
        frame_shift.setFixedWidth(140)

        label_shift = QLabel("Shift:", self)
        label_shift.setStyleSheet("""
            border: 0;
            color: white;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background: transparent;
            margin-left: 5px;
        """)

        self.entry_shift = QLineEdit(f"{self.shift_count:02}", self)
        self.entry_shift.setStyleSheet("""
            border: 2px;
            border-radius: 5px;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background-color: #555;
            height: 25px;
            width: 28px;
            margin-left: 50px;
        """)

        self.entry_shift.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.entry_shift.setReadOnly(True)

        self.entry_shift.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_shift_plus = QPushButton("+", self)
        btn_shift_plus.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 10px;
            margin-left: 8px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """)
        btn_shift_plus.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_shift_plus.clicked.connect(lambda: self.text_addons.shift_values("+"))

        btn_shift_minus = QPushButton("-", self)
        btn_shift_minus.setStyleSheet("""
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 10px;
            margin-left: 5px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """)
        btn_shift_minus.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_shift_minus.clicked.connect(lambda: self.text_addons.shift_values("-"))

        self.value_btn = QPushButton("Ori: 00000", self)
        self.value_btn.setStyleSheet("""
                QPushButton {
                    background-color: #444;
                    color: white;
                    font-family: 'Roboto', sans-serif;
                    font-size: 12px;
                    font-weight: 650;
                    padding: 6px;
                    border: none;
                    border-radius: 5px;
                    min-width: 65px;
                    margin-left: 10px;
                }
                QPushButton:hover {
                    background-color: #666;
                    color: #fff;
                }
                QPushButton:pressed{
                    background-color: #444;
                    color: white;
                }
                """)

        copy_btn = QPushButton("Copy", self)
        copy_btn.setStyleSheet(button_style)
        copy_btn.clicked.connect(lambda: self.text_addons.copy_values(False))

        paste_btn = QPushButton("Paste", self)
        paste_btn.setStyleSheet(button_style)
        paste_btn.clicked.connect(self.text_addons.paste_values)

        btn12 = QPushButton("Undo", self)
        btn12.setStyleSheet(button_style)
        btn12.clicked.connect(self.model.undo_changes)

        btn13 = QPushButton("Redo", self)
        btn13.setStyleSheet(button_style)
        btn13.clicked.connect(self.model.redo_changes)

        spacer = QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        left_grid_layout.addWidget(self.btn_lo_hi, 0, 0)
        left_grid_layout.addWidget(self.btn_hi_lo, 0, 1)
        left_grid_layout.addWidget(btn2, 0, 2)
        left_grid_layout.addWidget(btn3, 0, 3)

        mid_grid_layout.addWidget(self.sel_btn, 0, 0)

        mid_grid_layout.addWidget(frame_col, 0, 1, 1, 4)
        mid_grid_layout.addWidget(label_col, 0, 1)
        mid_grid_layout.addWidget(self.entry_col, 0, 1)
        mid_grid_layout.addWidget(btn_col_plus, 0, 2)
        mid_grid_layout.addWidget(btn_col_minus, 0, 3)

        mid_grid_layout.addItem(spacer, 0, 5)

        mid_grid_layout.addWidget(frame_shift, 0, 6, 1, 4)
        mid_grid_layout.addWidget(label_shift, 0, 6)
        mid_grid_layout.addWidget(self.entry_shift, 0, 6)
        mid_grid_layout.addWidget(btn_shift_plus, 0, 7)
        mid_grid_layout.addWidget(btn_shift_minus, 0, 8)

        mid_grid_layout.addWidget(self.value_btn, 0, 10)

        right_grid_layout.addWidget(copy_btn, 0, 0)
        right_grid_layout.addWidget(paste_btn, 0, 1)
        right_grid_layout.addWidget(btn12, 0, 2)
        right_grid_layout.addWidget(btn13, 0, 3)

        main_layout.addWidget(self.table_view, 0, 0, 1, 2)
        main_layout.addLayout(left_grid_layout, 1, 0, 1, 2)
        main_layout.addLayout(mid_grid_layout, 1, 0, 1, 2)
        main_layout.addLayout(right_grid_layout, 1, 0, 1, 2)

        left_grid_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        mid_grid_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        right_grid_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.tab1.setLayout(main_layout)

    def setup_tab2(self):
        main_layout = QGridLayout()

        left_grid_layout = QGridLayout()

        left_grid_layout.setContentsMargins(0, 0, 0, 0)
        left_grid_layout.setHorizontalSpacing(10)
        left_grid_layout.setVerticalSpacing(10)

        mid_grid_layout = QGridLayout()

        mid_grid_layout.setContentsMargins(0, 0, 0, 0)
        mid_grid_layout.setHorizontalSpacing(10)
        mid_grid_layout.setVerticalSpacing(10)

        right_grid_layout = QGridLayout()

        mid_grid_layout.setContentsMargins(0, 0, 0, 0)
        mid_grid_layout.setHorizontalSpacing(10)
        mid_grid_layout.setVerticalSpacing(10)

        button_style = """
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 50px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """

        outside_button_style = """
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;                    
            border: none;
            border-radius: 5px;
            min-width: 75px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """

        operation_style = """
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;                    
            border: none;
            border-radius: 5px;
            min-width: 10px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """

        btn_left = QPushButton("<", self.tab2)
        btn_left.setStyleSheet(button_style)
        btn_left.clicked.connect(self.mode2d.prev_page)

        btn_fast_left = QPushButton("<<", self.tab2)
        btn_fast_left.setStyleSheet(button_style)
        btn_fast_left.clicked.connect(lambda: self.mode2d.fast_movement("left"))

        btn_1 = QPushButton("Find Dialog", self.tab2)
        btn_1.setStyleSheet(outside_button_style)
        btn_1.clicked.connect(self.text_addons.open_find_dialog)

        btn_percentage_1 = QPushButton("%", self.tab2)
        btn_percentage_1.setStyleSheet(operation_style)
        btn_percentage_1.clicked.connect(lambda: self.mode2d.percentage(True, ""))
        btn_percentage_1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_minus = QPushButton("-", self.tab2)
        btn_minus.setStyleSheet(operation_style)
        btn_minus.clicked.connect(lambda: self.mode2d.percentage(False, "-"))
        btn_minus.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.entry_percentage = QLineEdit("00", self.tab2)
        self.entry_percentage.setStyleSheet("""
            border: 2px;
            border-radius: 6px;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 680;
            background-color: #555;
            height: 25px;
            width: 25px;
        """)

        self.entry_percentage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.entry_percentage.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_plus = QPushButton("+", self.tab2)
        btn_plus.setStyleSheet(operation_style)
        btn_plus.clicked.connect(lambda: self.mode2d.percentage(False, "+"))
        btn_plus.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        btn_percentage_2 = QPushButton("%", self.tab2)
        btn_percentage_2.setStyleSheet(operation_style)
        btn_percentage_2.clicked.connect(lambda: self.mode2d.percentage(True, ""))
        btn_percentage_2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.value_btn_2d = QPushButton("Value: 00000", self.tab2)
        self.value_btn_2d.setStyleSheet(outside_button_style)

        btn_fast_right = QPushButton(">>", self.tab2)
        btn_fast_right.setStyleSheet(button_style)
        btn_fast_right.clicked.connect(lambda: self.mode2d.fast_movement("right"))

        btn_right = QPushButton(">", self.tab2)
        btn_right.setStyleSheet(button_style)
        btn_right.clicked.connect(self.mode2d.next_page)

        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)

        self.fig.patch.set_facecolor('#333')
        self.ax.set_facecolor('#333')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.canvas = FigureCanvas(self.fig)

        self.canvas.setStyleSheet("border: 0;")

        self.canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.canvas.mpl_connect("button_press_event", self.mode2d.on_canvas_click)  # change later
        self.canvas.mpl_connect("key_press_event", self.mode2d.on_key_press_2d)  # change later

        left_grid_layout.addWidget(btn_left, 0, 0)
        left_grid_layout.addWidget(btn_fast_left, 0, 1)

        mid_grid_layout.addWidget(btn_1, 0, 0)

        spacer = QSpacerItem(25, 1, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        mid_grid_layout.addItem(spacer, 0, 1)

        mid_grid_layout.addWidget(btn_percentage_1, 0, 2)
        mid_grid_layout.addWidget(btn_minus, 0, 3)
        mid_grid_layout.addWidget(self.entry_percentage, 0, 4)
        mid_grid_layout.addWidget(btn_plus, 0, 5)
        mid_grid_layout.addWidget(btn_percentage_2, 0, 6)

        mid_grid_layout.addItem(spacer, 0, 7)

        mid_grid_layout.addWidget(self.value_btn_2d, 0, 8)

        right_grid_layout.addWidget(btn_fast_right, 0, 0)
        right_grid_layout.addWidget(btn_right, 0, 1)


        main_layout.addWidget(self.canvas, 0, 0, 1, 2)
        main_layout.addLayout(left_grid_layout, 1, 0, 1, 2)
        main_layout.addLayout(mid_grid_layout, 1, 0, 1, 2)
        main_layout.addLayout(right_grid_layout, 1, 0, 1, 2)

        left_grid_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        mid_grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_grid_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.tab2.setLayout(main_layout)

    def setup_tab3(self):
        main_layout = QGridLayout()

        left_grid_layout = QGridLayout()

        left_grid_layout.setContentsMargins(0, 0, 0, 0)
        left_grid_layout.setHorizontalSpacing(10)
        left_grid_layout.setVerticalSpacing(10)

        mid_grid_layout = QGridLayout()

        mid_grid_layout.setContentsMargins(0, 0, 0, 0)
        mid_grid_layout.setHorizontalSpacing(10)
        mid_grid_layout.setVerticalSpacing(10)

        right_grid_layout = QGridLayout()

        mid_grid_layout.setContentsMargins(0, 0, 0, 0)
        mid_grid_layout.setHorizontalSpacing(10)
        mid_grid_layout.setVerticalSpacing(10)

        button_style = """
        QPushButton {
            background-color: #444;
            color: white;
            font-family: 'Roboto', sans-serif;
            font-size: 12px;
            font-weight: 650;
            padding: 6px;
            border: none;
            border-radius: 5px;
            min-width: 65px;
        }
        QPushButton:hover {
            background-color: #666;
            color: #fff;
        }
        QPushButton:pressed{
            background-color: #444;
            color: white;
        }
        """

        btn0 = QPushButton("Copy Map", self)
        btn0.setStyleSheet(button_style)
        btn0.clicked.connect(self.mode3d.copy_map_values)

        btn1 = QPushButton("Copy Selected", self)
        btn1.setStyleSheet(button_style)
        btn1.clicked.connect(self.mode3d.copy_selected_3d)

        btn2 = QPushButton("Copy X Axis", self)
        btn2.setStyleSheet(button_style)
        btn2.clicked.connect(self.mode3d.copy_x_axis)

        btn3 = QPushButton("Copy Y Axis", self)
        btn3.setStyleSheet(button_style)
        btn3.clicked.connect(self.mode3d.copy_y_axis)

        btn4 = QPushButton("Update", self)
        btn4.setStyleSheet(button_style)
        btn4.clicked.connect(self.maps.update_3d_from_text)

        self.diff_btn_3d = QPushButton("Diff: 00000", self)
        self.diff_btn_3d.setStyleSheet(button_style)

        frame_row = QFrame(self)
        frame_row.setFrameShape(QFrame.Shape.StyledPanel)
        frame_row.setFrameShadow(QFrame.Shadow.Raised)
        frame_row.setStyleSheet("""
            border: 2px solid #888;
            border-radius: 5px;
        """)

        frame_row.setFixedHeight(35)
        frame_row.setFixedWidth(75)

        label_row = QLabel("Row:", frame_row)
        label_row.setStyleSheet("""
            border: 0;
            color: white;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background: transparent;
            margin-left: 5px;
        """)

        self.entry_row_3d = QLineEdit(self)
        self.entry_row_3d.setStyleSheet("""
            border: 2px;
            border-radius: 5px;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background-color: #555;
            height: 25px;
            width: 28px;
            margin-left: 41px;
        """)

        self.entry_row_3d.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.entry_row_3d.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        frame_col = QFrame(self)
        frame_col.setFrameShape(QFrame.Shape.StyledPanel)
        frame_col.setFrameShadow(QFrame.Shadow.Raised)
        frame_col.setStyleSheet("""
            border: 2px solid #888;
            border-radius: 5px;
        """)

        frame_col.setFixedHeight(35)
        frame_col.setFixedWidth(75)

        label_col = QLabel("Col:", self)
        label_col.setStyleSheet("""
            border: 0;
            color: white;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background: transparent;
            margin-left: 5px;
        """)

        self.entry_col_3d = QLineEdit(self)
        self.entry_col_3d.setStyleSheet("""
            border: 2px;
            border-radius: 5px;
            font-family: 'Roboto';
            font-size: 12px;
            font-weight: 650;
            background-color: #555;
            height: 25px;
            width: 28px;
            margin-left: 41px;
        """)

        self.entry_col_3d.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.entry_col_3d.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.entry_row_3d.setReadOnly(True)
        self.entry_col_3d.setReadOnly(True)

        value_btn = QPushButton("Value", self)
        value_btn.setStyleSheet(button_style)
        value_btn.clicked.connect(self.maps.value_changer_dialog)

        write_map_btn = QPushButton("Write Map", self)
        write_map_btn.setStyleSheet(button_style)
        write_map_btn.clicked.connect(self.maps.write_map)

        btn10 = QPushButton("Paste X Axis", self)
        btn10.setStyleSheet(button_style)
        btn10.clicked.connect(lambda: self.mode3d.paste_x_data(False, [], False))

        btn11 = QPushButton("Paste Y Axis", self)
        btn11.setStyleSheet(button_style)
        btn11.clicked.connect(lambda: self.mode3d.paste_y_data(False, [], False))

        btn12 = QPushButton("Paste Selected", self)
        btn12.setStyleSheet(button_style)
        btn12.clicked.connect(self.mode3d.paste_selected)

        btn13 = QPushButton("Paste Map", self)
        btn13.setStyleSheet(button_style)
        btn13.clicked.connect(lambda: self.mode3d.paste_data(False, [], 0, 0, False, ""))

        left_grid_layout.addWidget(btn0, 0, 0)
        left_grid_layout.addWidget(btn1, 0, 1)
        left_grid_layout.addWidget(btn2, 0, 2)
        left_grid_layout.addWidget(btn3, 0, 3)

        mid_grid_layout.addWidget(btn4, 0, 0)
        mid_grid_layout.addWidget(self.diff_btn_3d, 0, 1)

        mid_grid_layout.addWidget(frame_row, 0, 2)
        mid_grid_layout.addWidget(label_row, 0, 2)
        mid_grid_layout.addWidget(self.entry_row_3d, 0, 2)

        mid_grid_layout.addWidget(frame_col, 0, 3)
        mid_grid_layout.addWidget(label_col, 0, 3)
        mid_grid_layout.addWidget(self.entry_col_3d, 0, 3)

        mid_grid_layout.addWidget(value_btn, 0, 4)
        mid_grid_layout.addWidget(write_map_btn, 0, 5)

        right_grid_layout.addWidget(btn10, 0, 0)
        right_grid_layout.addWidget(btn11, 0, 1)
        right_grid_layout.addWidget(btn12, 0, 2)
        right_grid_layout.addWidget(btn13, 0, 3)

        self.box_layout = CustomTableWidget(self)
        self.box_layout.setRowCount(self.num_rows_3d)
        self.box_layout.setColumnCount(self.num_columns_3d)

        self.box_layout.setStyleSheet("""
            QTableView {
                background-color: #333;
            }
            QTableView::item:selected {
                background-color: #5b9bf8;
                color: white;
            }
            QHeaderView::section {
                background-color: #363636;
                color: white;
            } 
        """)

        font = QFont("Cantarell", 11)
        self.box_layout.setFont(font)

        self.box_layout.itemChanged.connect(self.mode3d.validate_cell_input)
        self.box_layout.itemSelectionChanged.connect(self.mode3d.on_selection_3d)

        self.mode3d.set_default()

        self.box_layout.horizontalHeader().sectionDoubleClicked.connect(self.mode3d.edit_horizontal_header)
        self.box_layout.verticalHeader().sectionDoubleClicked.connect(self.mode3d.edit_vertical_header)

        self.box_layout.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.box_layout.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.box_layout.verticalHeader().setFixedWidth(55)

        main_layout.addWidget(self.box_layout, 0, 0, 1, 2)

        main_layout.addLayout(left_grid_layout, 1, 0, 1, 2)
        main_layout.addLayout(mid_grid_layout, 1, 0, 1, 2)
        main_layout.addLayout(right_grid_layout, 1, 0, 1, 2)

        left_grid_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        mid_grid_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
        right_grid_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self.tab3.setLayout(main_layout)

    def setup_tab4(self):
        self.map_list = CustomListBox(self)
        self.map_list.setStyleSheet("background-color: #333; color: white; font-size: 10pt;")
        self.map_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        self.map_list.itemDoubleClicked.connect(self.maps.on_double_click)

        layout = QVBoxLayout(self.tab4)
        layout.addWidget(self.map_list)

        self.tab4.setLayout(layout)


    def create_menu_bar(self):
        menubar = self.menuBar()

        menu_bar_style = ("""
        QMenuBar {
            background-color: #333;
            color: white;
        }
        QMenuBar::item {
            padding: 10px;
            background-color: #333;
        }
        QMenuBar::item:selected {
            background-color: #555;
        }
        QMenuBar::item:pressed {
            background-color: #777;
        }
        QMenu {
            background-color: #333;
            color: white;
        }
        QMenu::item:selected {
            background-color: #555;
        }
        QMenu::item:pressed {
            background-color: #777;
        }
        """)

        menubar.setStyleSheet(menu_bar_style)

        file_menu = menubar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.text_view_.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.text_view_.save_file)
        file_menu.addAction(save_action)

        options_menu = menubar.addMenu("Options")

        find_action = QAction("Find", self)
        options_menu.addAction(find_action)
        find_action.triggered.connect(self.text_addons.open_find_dialog)

        import_action = QAction("Import", self)
        options_menu.addAction(import_action)
        import_action.triggered.connect(self.text_addons.import_file)

        difference_action = QAction("Difference", self)
        options_menu.addAction(difference_action)
        difference_action.triggered.connect(self.text_addons.open_difference_dialog)

        value_changer_action = QAction("Value Changer", self)
        options_menu.addAction(value_changer_action)
        value_changer_action.triggered.connect(self.text_addons.open_value_dialog)

        find_hex_action = QAction("Find Hex Address", self)
        options_menu.addAction(find_hex_action)
        find_hex_action.triggered.connect(self.text_addons.open_hex_address_dialog)

        restart_map_search = QAction("Restart Map Search", self)
        options_menu.addAction(restart_map_search)
        restart_map_search.triggered.connect(lambda: self.maps.start_potential_map_search(True))

        map_pack_menu = menubar.addMenu("Mappack")

        import_map_pack_action = QAction("Import Mappack", self)
        map_pack_menu.addAction(import_map_pack_action)
        import_map_pack_action.triggered.connect(self.maps.import_map)

        export_map_pack_action = QAction("Export Mappack", self)
        map_pack_menu.addAction(export_map_pack_action)
        export_map_pack_action.triggered.connect(self.maps.export_map)

    def clean_up(self):
        file_path = "mappack.mp"
        if os.path.exists(file_path):
            os.remove(file_path)

    def closeEvent(self, event):
        if self.file_path:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setWindowTitle("Save Changes?")
            msg_box.setText("Do you really want to exit without saving?")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            response = msg_box.exec()

            if response == QMessageBox.StandardButton.Yes:
                self.exit_app()
            else:
                event.ignore()
        else:
            self.exit_app()

    def exit_app(self):
        self.tk_win_manager.kill_tkinter_window()
        time.sleep(0.001)
        self.clean_up()
        self.close()

class QTableModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.linols = parent
        self._data = [list(row) for row in data]
        self._vertical_header_labels = []  # Initialize vertical header labels
        self.undo_stack = []
        self.redo_stack = []

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index: QModelIndex, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return f"{value:05}" if value is not None else ""

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        value = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.ForegroundRole:
            color = self.linols.text_addons.highlight_difference(value, index.row(), index.column())
            if color == "blue":
                return QColor(Qt.GlobalColor.blue)
            elif color == "red":
                return QColor(Qt.GlobalColor.red)
            elif color == "default":
                return QColor(Qt.GlobalColor.white)

        if role == Qt.ItemDataRole.BackgroundRole: # highlight user maps
            index = (index.row() * self.linols.columns) + index.column()

            if self.linols.map_list_counter > 0:
                # user creted maps
                for i in range(len(self.linols.start_index_maps)):
                    down_limit = self.linols.start_index_maps[i]
                    up_limit = self.linols.end_index_maps[i]
                    if down_limit <= index <= up_limit:
                        return QColor(133, 215, 242, 150) # light blue

            # potential maps
            for i in range(len(self.linols.potential_maps_start)):
                down_limit = self.linols.potential_maps_start[i]
                up_limit = self.linols.potential_maps_end[i]
                if down_limit <= index <= up_limit:
                    return QColor(1, 133, 123, 150) # teal green

    def setData(self, index: QModelIndex, value, role):
        if role == Qt.ItemDataRole.EditRole:
            row, col = index.row(), index.column()
            try:
                new_value = int(value)
                old_value = self._data[row][col]
                if (new_value < 0) or (new_value > 65535):
                    self._data[row][col] = self.linols.text_addons.revert_value(row, col)
                else:
                    self._data[row][col] = new_value
                    self.redraw_canvas_2d(row, col, new_value)
                self.undo_stack.append((row, col, old_value))
                self.redo_stack.clear()
                self.dataChanged.emit(index, index)
            except ValueError:
                return False
        return True

    def redraw_canvas_2d(self, row, col, value):
        self.linols.current_values = list(self.linols.current_values)
        index = (row * self.linols.columns) + col

        self.linols.current_values[index] = value

        self.linols.sync_2d_scroll = True
        self.linols.mode2d.draw_canvas(self.linols)

    def flags(self, index: QModelIndex):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def set_data(self, data):
        self._data = [list(row) for row in data]
        self.layoutChanged.emit()

    def setVerticalHeaderLabels(self, labels):
        self._vertical_header_labels = labels
        self.headerDataChanged.emit(Qt.Orientation.Vertical, 0, self.rowCount() - 1)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Vertical:
                return self._vertical_header_labels[section] if section < len(self._vertical_header_labels) else ""
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    def get_all_data(self):
        return self._data

    def undo_changes(self):
        if not self.linols.file_path:
            QMessageBox.warning(None, "Warning", "No file is currently open. Please open a file first.")
            return

        if not self.undo_stack:
            return

        row, col, old_value = self.undo_stack.pop()

        current_value = self._data[row][col]
        self.redo_stack.append((row, col, current_value))

        self._data[row][col] = old_value

        index = self.index(row, col)
        self.dataChanged.emit(index, index)

    def redo_changes(self):
        if not self.linols.file_path:
            QMessageBox.warning(None, "Warning", "No file is currently open. Please open a file first.")
            return

        if not self.redo_stack:
            return

        row, col, old_value = self.redo_stack.pop()

        current_value = self._data[row][col]
        self.undo_stack.append((row, col, current_value))

        self._data[row][col] = old_value

        index = self.index(row, col)
        self.dataChanged.emit(index, index)

class CustomTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.linols = parent
        self.verticalScrollBar().valueChanged.connect(self.on_scroll)

        font = QFont("Cantarell", 10)
        self.verticalHeader().setFont(font)

    def on_scroll(self):
        if not self.linols.tab1_selected:
            return

        # Calculate the first visible row index by checking the geometry of each row
        visible_rect = self.viewport().geometry()
        first_visible_row = self.indexAt(visible_rect.topLeft()).row()

        frame_before = self.linols.current_frame

        index = first_visible_row * self.linols.columns
        frame = self.linols.num_rows * self.linols.columns
        frames_num = index // frame
        self.linols.current_frame = frames_num * frame

        if frame_before != self.linols.current_frame:
            self.linols.sync_2d_scroll = True
            self.linols.mode2d.draw_canvas(self.linols)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() in [Qt.Key.Key_PageUp, Qt.Key.Key_PageDown]: # Track when Page Up or Page Down is pressed
            self.on_scroll()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.linols.text_addons.on_selection()
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.on_right_click(event)
        super().mousePressEvent(event)

    def on_right_click(self, event):
        selection_model = self.linols.table_view.selectionModel()
        selected_indexes_count = len(selection_model.selectedIndexes())

        if selected_indexes_count != 1:
            return

        right_menu = QMenu(self.parent())

        copy_hex = QAction("Copy Hex Address", self)
        open_map_action = QAction("Open Map", self)
        add_potential_map_action = QAction("Add Potential Map", self)
        remove_potential_map_action = QAction("Remove Potential Map", self)

        copy_hex.triggered.connect(self.linols.text_addons.copy_hex_address)
        open_map_action.triggered.connect(self.linols.maps.open_map_right_click)
        add_potential_map_action.triggered.connect(self.linols.maps.add_potential_map)
        remove_potential_map_action.triggered.connect(self.linols.maps.remove_potential_map)

        right_menu.addAction(copy_hex)
        right_menu.addAction(open_map_action)
        right_menu.addAction(add_potential_map_action)
        right_menu.addAction(remove_potential_map_action)

        pos = event.globalPosition().toPoint()

        right_menu.exec(pos)

    def keyPressEvent(self, event):
        if event.key() == 16777274: # check if the F11 is pressed
            self.on_f11_pressed()
        else:
            super().keyPressEvent(event)

    def on_f11_pressed(self):
        selection_model = self.linols.table_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        for item in selected_indexes:
            row = item.row()
            col = item.column()

            index_unpacked = (row * self.linols.columns) + col

            index = self.linols.model.index(row, col)

            self.linols.model.setData(index, self.linols.unpacked[index_unpacked], Qt.ItemDataRole.EditRole)

class CustomListBox(QListWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        remove_action = QAction("Remove", self)
        remove_action.triggered.connect(self.ui.maps.remove_item)
        context_menu.addAction(remove_action)

        context_menu.exec(event.globalPos())

class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = parent

        font = QFont("Cantarell", 10)
        self.verticalHeader().setFont(font)
        self.horizontalHeader().setFont(font)

        self.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(self.showHorizontalHeaderContextMenu)

        self.verticalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.verticalHeader().customContextMenuRequested.connect(self.showVerticalHeaderContextMenu)


    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        action_prop = QAction("Map Properties", self)
        context_menu.addAction(action_prop)
        action_sign_values = QAction("Sign Values 3D", self)
        context_menu.addAction(action_sign_values)

        action_prop.triggered.connect(lambda: self.ui.maps.map_properties_dialog("map"))
        action_sign_values.triggered.connect(self.ui.maps.sign_values)

        context_menu.exec(event.globalPos())

    def showHorizontalHeaderContextMenu(self, pos: QPoint):
        context_menu = QMenu(self)
        action = context_menu.addAction(f"X-Axis Properties")
        action.triggered.connect(lambda: self.ui.maps.map_properties_dialog("x"))
        context_menu.exec(self.horizontalHeader().mapToGlobal(pos))

    def showVerticalHeaderContextMenu(self, pos: QPoint):
        context_menu = QMenu(self)
        action = context_menu.addAction(f"Y-Axis Properties")
        action.triggered.connect(lambda: self.ui.maps.map_properties_dialog("y"))
        context_menu.exec(self.verticalHeader().mapToGlobal(pos))