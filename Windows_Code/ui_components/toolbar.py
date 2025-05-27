from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QToolBar, QPushButton, QStyle, QWidget, QGridLayout
from PyQt6.QtCore import Qt, QSize, QByteArray
from PyQt6.QtSvg import QSvgRenderer
import sys
import os

svg_arrow_circle = '''
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="white" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="m12.75 15 3-3m0 0-3-3m3 3h-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
</svg>
'''

svg_differences = '''
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M9 3H3.6C3.26863 3 3 3.26863 3 3.6V20.4C3 20.7314 3.26863 21 3.6 21H9M9 3V21M9 3H15M9 21H15M15 3H20.4C20.7314 3 21 3.26863 21 3.6V20.4C21 20.7314 20.7314 21 20.4 21H15M15 3V21" stroke="#ffffff" stroke-width="1.5"></path> </g></svg>
'''

next_value_svg = '''
<svg fill="#ffffff" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M 2.9281 44.4947 C 3.7618 44.4947 4.4531 44.2304 5.2665 43.7424 L 25.9869 31.5420 C 27.1053 30.8913 27.7153 30.1592 27.9389 29.3052 L 27.9389 41.0176 C 27.9389 43.2747 29.2810 44.4947 30.8671 44.4947 C 31.7007 44.4947 32.3921 44.2304 33.2055 43.7424 L 53.9461 31.5420 C 55.3695 30.6879 56 29.6916 56 28.5122 C 56 27.3531 55.3695 26.3568 53.9461 25.5028 L 33.2055 13.3023 C 32.3921 12.8143 31.7007 12.5500 30.8671 12.5500 C 29.2810 12.5500 27.9389 13.7700 27.9389 16.0271 L 27.9389 27.7395 C 27.7153 26.8855 27.1053 26.1535 25.9869 25.5028 L 5.2665 13.3023 C 4.4328 12.8143 3.7618 12.5500 2.9281 12.5500 C 1.3420 12.5500 0 13.7700 0 16.0271 L 0 41.0176 C 0 43.2747 1.3420 44.4947 2.9281 44.4947 Z M 3.8228 40.7329 C 3.5178 40.7329 3.2738 40.5499 3.2738 40.1229 L 3.2738 16.9218 C 3.2738 16.4948 3.5178 16.3117 3.8228 16.3117 C 3.9651 16.3117 4.1075 16.3728 4.3108 16.4745 L 23.6485 27.9428 C 23.9332 28.1055 24.0958 28.2479 24.0958 28.5122 C 24.0958 28.7969 23.9332 28.9392 23.6485 29.1019 L 4.3108 40.5703 C 4.1278 40.6923 3.9651 40.7329 3.8228 40.7329 Z M 31.7618 40.7329 C 31.4568 40.7329 31.2127 40.5499 31.2127 40.1229 L 31.2127 16.9218 C 31.2127 16.4948 31.4568 16.3117 31.7618 16.3117 C 31.9041 16.3117 32.0464 16.3728 32.2498 16.4745 L 51.5874 27.9428 C 51.8722 28.1055 52.0346 28.2479 52.0346 28.5122 C 52.0346 28.7969 51.8722 28.9392 51.5874 29.1019 L 32.2498 40.5703 C 32.0668 40.6923 31.9041 40.7329 31.7618 40.7329 Z"></path></g></svg>
'''

previous_value_svg = '''
<svg fill="#ffffff" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M 25.1218 44.5009 C 26.7084 44.5009 28.0509 43.2804 28.0509 41.0225 L 28.0509 29.3058 C 28.2747 30.1601 28.9053 30.8924 30.0037 31.5434 L 50.7318 43.7483 C 51.5454 44.2365 52.2369 44.5009 53.0709 44.5009 C 54.6577 44.5009 56 43.2804 56 41.0225 L 56 16.0228 C 56 13.7649 54.6577 12.5444 53.0709 12.5444 C 52.2369 12.5444 51.5658 12.8088 50.7318 13.2970 L 30.0037 25.5020 C 28.8849 26.1529 28.2747 26.8852 28.0509 27.7395 L 28.0509 16.0228 C 28.0509 13.7649 26.7084 12.5444 25.1218 12.5444 C 24.2877 12.5444 23.6165 12.8088 22.7825 13.2970 L 2.0545 25.5020 C .6102 26.3563 0 27.3530 0 28.5125 C 0 29.6923 .6102 30.6890 2.0545 31.5434 L 22.7825 43.7483 C 23.5962 44.2365 24.2877 44.5009 25.1218 44.5009 Z M 24.2267 40.7377 C 24.0843 40.7377 23.9216 40.6970 23.7386 40.5750 L 4.3938 29.1024 C 4.1090 28.9396 3.9463 28.7973 3.9463 28.5125 C 3.9463 28.2481 4.1090 28.1057 4.3938 27.9429 L 23.7386 16.4703 C 23.9419 16.3686 24.0843 16.3076 24.2267 16.3076 C 24.5318 16.3076 24.7760 16.4907 24.7760 16.9178 L 24.7760 40.1275 C 24.7760 40.5546 24.5318 40.7377 24.2267 40.7377 Z M 52.1761 40.7377 C 52.0540 40.7377 51.8911 40.6970 51.6878 40.5750 L 32.3430 29.1024 C 32.0582 28.9396 31.9158 28.7973 31.9158 28.5125 C 31.9158 28.2481 32.0582 28.1057 32.3430 27.9429 L 51.6878 16.4703 C 51.8911 16.3686 52.0540 16.3076 52.1761 16.3076 C 52.4810 16.3076 52.7252 16.4907 52.7252 16.9178 L 52.7252 40.1275 C 52.7252 40.5546 52.4810 40.7377 52.1761 40.7377 Z"></path></g></svg>
'''

last_value_svg = '''
<svg fill="#ffffff" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M 2.7616 43.7432 C 3.5480 43.7432 4.2000 43.4939 4.9671 43.0336 L 24.5096 31.5267 C 25.5644 30.9130 26.1398 30.2034 26.3507 29.4171 L 26.3507 40.4446 C 26.3507 42.5925 27.6165 43.7432 29.1124 43.7432 C 29.8987 43.7432 30.5508 43.4939 31.3179 43.0336 L 50.8795 31.5267 C 51.9152 30.9130 52.4906 30.2034 52.7208 29.4171 L 52.7208 42.9185 C 52.7208 43.8199 53.4494 44.5103 54.3508 44.5103 C 55.2522 44.5103 56 43.8199 56 42.9185 L 56 14.4390 C 56 13.5376 55.2522 12.8281 54.3508 12.8281 C 53.4494 12.8281 52.7208 13.5376 52.7208 14.4390 L 52.7208 27.9212 C 52.4906 27.1349 51.9152 26.4253 50.8795 25.8116 L 31.3179 14.3048 C 30.5508 13.8445 29.8987 13.5952 29.1124 13.5952 C 27.6165 13.5952 26.3507 14.7459 26.3507 16.8938 L 26.3507 27.9212 C 26.1398 27.1349 25.5644 26.4253 24.5096 25.8116 L 4.9671 14.3048 C 4.1808 13.8445 3.5480 13.5952 2.7616 13.5952 C 1.2657 13.5952 0 14.7459 0 16.8938 L 0 40.4446 C 0 42.5925 1.2657 43.7432 2.7616 43.7432 Z M 3.6055 40.1952 C 3.3178 40.1952 3.0877 40.0035 3.0877 39.6199 L 3.0877 17.7185 C 3.0877 17.3349 3.3178 17.1431 3.6055 17.1431 C 3.7397 17.1431 3.8740 17.2007 4.0657 17.3157 L 22.3042 28.1322 C 22.5727 28.2856 22.7261 28.4007 22.7261 28.6692 C 22.7261 28.9185 22.5727 29.0528 22.3042 29.2062 L 4.0657 40.0226 C 3.8932 40.1377 3.7397 40.1952 3.6055 40.1952 Z M 29.9562 40.1952 C 29.6686 40.1952 29.4384 40.0035 29.4384 39.6199 L 29.4384 17.7185 C 29.4384 17.3349 29.6686 17.1431 29.9562 17.1431 C 30.0905 17.1431 30.2247 17.2007 30.4165 17.3157 L 48.6548 28.1322 C 48.9235 28.2856 49.0767 28.4007 49.0767 28.6692 C 49.0767 28.9185 48.9235 29.0528 48.6548 29.2062 L 30.4165 40.0226 C 30.2439 40.1377 30.0905 40.1952 29.9562 40.1952 Z"></path></g></svg>
'''

first_value_svg = '''
<svg fill="#ffffff" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M 1.6493 44.5103 C 2.5507 44.5103 3.2795 43.8199 3.2795 42.9185 L 3.2795 29.4171 C 3.2219 29.1678 3.1835 28.9185 3.1835 28.6692 C 3.1835 28.4007 3.2219 28.1514 3.2795 27.9212 L 3.2795 14.4390 C 3.2795 13.5376 2.5507 12.8281 1.6493 12.8281 C .7479 12.8281 0 13.5376 0 14.4390 L 0 42.9185 C 0 43.8199 .7479 44.5103 1.6493 44.5103 Z M 26.8686 43.7432 C 28.3836 43.7432 29.6302 42.5925 29.6302 40.4446 L 29.6302 29.4171 C 29.8603 30.2034 30.4357 30.9130 31.4713 31.5267 L 51.0138 43.0336 C 51.8001 43.4939 52.4521 43.7432 53.2384 43.7432 C 54.7345 43.7432 56 42.5925 56 40.4446 L 56 16.8938 C 56 14.7459 54.7345 13.5952 53.2384 13.5952 C 52.4521 13.5952 51.8001 13.8445 51.0138 14.3048 L 31.4713 25.8116 C 30.4357 26.4253 29.8603 27.1349 29.6302 27.9212 L 29.6302 16.8938 C 29.6302 14.7459 28.3836 13.5952 26.8686 13.5952 C 26.1014 13.5952 25.4494 13.8445 24.6630 14.3048 L 5.1206 25.8116 C 4.0849 26.4253 3.5096 27.1349 3.2795 27.9212 L 3.2795 29.4171 C 3.5096 30.2034 4.0849 30.9130 5.1206 31.5267 L 24.6630 43.0336 C 25.4494 43.4939 26.1014 43.7432 26.8686 43.7432 Z M 26.0439 40.1952 C 25.9096 40.1952 25.7562 40.1377 25.5644 40.0226 L 7.3452 29.2062 C 7.0767 29.0528 6.9233 28.9185 6.9233 28.6692 C 6.9233 28.4007 7.0767 28.2856 7.3452 28.1322 L 25.5644 17.3157 C 25.7562 17.2007 25.9096 17.1431 26.0439 17.1431 C 26.3124 17.1431 26.5617 17.3349 26.5617 17.7185 L 26.5617 39.6199 C 26.5617 40.0035 26.3124 40.1952 26.0439 40.1952 Z M 52.3948 40.1952 C 52.2605 40.1952 52.1069 40.1377 51.9152 40.0226 L 33.6960 29.2062 C 33.4275 29.0528 33.2740 28.9185 33.2740 28.6692 C 33.2740 28.4007 33.4275 28.2856 33.6960 28.1322 L 51.9152 17.3157 C 52.1069 17.2007 52.2605 17.1431 52.3948 17.1431 C 52.6630 17.1431 52.9125 17.3349 52.9125 17.7185 L 52.9125 39.6199 C 52.9125 40.0035 52.6630 40.1952 52.3948 40.1952 Z"></path></g></svg>
'''


class ToolbarWidget(QWidget):
    def __init__(self, ui):
        super().__init__()

        self.ui = ui

        self.setMinimumWidth(900)

        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #333;
                spacing: 4px;
                padding: 0px;
            }
            QPushButton {
                font-family: 'Roboto', sans-serif;
                font-size: 12px;
                font-weight: 650;
                background-color: #444;
                color: white;
                border: 1px solid #555;
                padding: 6px 10px;
                margin-top: 4px;
                margin-bottom: 4px;
                height: 18px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed{
                background-color: #444;
            }
            QPushButton:disabled {
            background-color: #555;
            color: #aaa;
            }
        """)

        layout = QGridLayout(self)
        layout.addWidget(toolbar)

        def icon_button(icon, tooltip="", message=""):
            btn = QPushButton()
            btn.setIcon(icon)
            btn.setToolTip(tooltip)
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(lambda: self.manage_message(message))
            return btn

        def add_space(size):
            spacer = QWidget()
            spacer.setFixedWidth(size)
            toolbar.addWidget(spacer)

        style = self.style()

        add_space(1)

        nav_buttons = [
            (self.svg_to_icon(first_value_svg), "First difference (E)", "FirstValue"),
            (self.svg_to_icon(previous_value_svg), "Previous difference (V)", "PrevValue"),
            (self.svg_to_icon(svg_differences), "Differences (CTRL + U)", "DiffDialog"),
            (self.svg_to_icon(next_value_svg), "Next difference (N)", "NextValue"),
            (self.svg_to_icon(last_value_svg), "Last difference (L)", "LastValue"),
        ]
        for icon, tip, message in nav_buttons:
            toolbar.addWidget(icon_button(icon, tip, message))

        add_space(2)

        self.ui.btn_lo_hi = QPushButton("LOHI")
        self.ui.btn_lo_hi.setEnabled(False)
        self.ui.btn_lo_hi.clicked.connect(lambda: self.ui.text_view_.ask_change_display_mode("low_high"))
        toolbar.addWidget(self.ui.btn_lo_hi)

        self.ui.btn_hi_lo = QPushButton("HILO")
        self.ui.btn_hi_lo.clicked.connect(lambda: self.ui.text_view_.ask_change_display_mode("high_low"))
        toolbar.addWidget(self.ui.btn_hi_lo)

        add_space(2)

        search_buttons = [
            ('Search', style.standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView), "Search"),
            ('Go to Hex Address', self.svg_to_icon(svg_arrow_circle), "Hex"),
        ]

        for tip, icon, message in search_buttons:
            btn = icon_button(icon, tip, message)
            toolbar.addWidget(btn)

        add_space(2)

        col_icons = [
            ('More columns (M)', QIcon(self.resource_path("ui_components/col_add.png")), "Col+"),
            ('Less columns (W)', QIcon(self.resource_path("ui_components/col_remove.png")), "Col-"),
            ('Shift Columns (+)', QIcon(self.resource_path("ui_components/shift_col+.png")), "Shift+"),
            ('Shift Columns (-)', QIcon(self.resource_path("ui_components/shift_col-.png")), "Shift-"),
        ]

        for tip, icon, message in col_icons:
            btn = icon_button(icon, tip, message)
            toolbar.addWidget(btn)

        add_space(1)

    def svg_to_icon(self, svg_data: str, size: QSize = QSize(64, 64)) -> QIcon:
        renderer = QSvgRenderer(QByteArray(svg_data.encode()))
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    def manage_message(self, message):
        if message == "Search":
            self.ui.text_addons.open_find_dialog()
        elif message == "Hex":
            self.ui.text_addons.open_hex_address_dialog()
        elif message == "Col+":
            self.ui.text_addons.adjust_columns("+")
        elif message == "Col-":
            self.ui.text_addons.adjust_columns("-")
        elif message == "Shift+":
            self.ui.text_addons.shift_values("+")
        elif message == "Shift-":
            self.ui.text_addons.shift_values("-")
        elif message == "DiffDialog":
            self.ui.text_addons.open_difference_dialog()
        elif message == "NextValue":
            self.ui.mode2d.value_changes_skipping(True)
        elif message == "PrevValue":
            self.ui.mode2d.value_changes_skipping(False)
        elif message == "FirstValue":
            self.ui.mode2d.first_last_changed_value(True)
        elif message == "LastValue":
            self.ui.mode2d.first_last_changed_value(False)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)