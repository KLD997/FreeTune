from tkinter import *
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import numpy as np
import queue

class TkWindowManager:
    def __init__(self, ui):
        self.ui = ui
        self.tk_root = None
        self.tk_thread = None
        self.shutdown_event = threading.Event()

        self.tkinter_available = False
        self.tk_win = None

        self.queue = queue.Queue()

    def call_update_3d(self):
        if not self.tkinter_available:
            return

        self.queue.put('update_3d')

    def open_tkinter_window(self):
        if self.tk_thread and self.tk_thread.is_alive():
            return

        self.shutdown_event.clear()

        screen = QApplication.primaryScreen()
        geometry = screen.geometry()
        screen_width = geometry.width()
        screen_height = geometry.height()

        width_calc = screen_width - int(screen_width / 2)

        x = screen_width // 2 + width_calc // 4
        y = int(screen_height / 8)

        self.create_3d_figure()

        def run_tk():
            self.tk_root = Tk()
            self.tk_root.geometry(f"+{x}+{y}")
            self.tk_win = TkinterWindow(self.tk_root, self.ui, self)
            self.tkinter_available = True

            def on_close():
                self.shutdown_event.set()

            self.tk_root.protocol("WM_DELETE_WINDOW", on_close)

            while not self.shutdown_event.is_set():
                self.tk_root.update()
                if not self.queue.empty():
                    msg = self.queue.get()
                    if msg == 'update_3d':
                        self.tk_win.update_3d_view()

            self.tk_root.destroy()
            self.tk_root = None

        self.tk_thread = threading.Thread(target=run_tk, daemon=True)
        self.tk_thread.start()

    def kill_tkinter_window(self):
        if self.tk_root and self.tk_thread and self.tk_thread.is_alive():
            self.shutdown_event.set()

    def create_3d_figure(self):
        self.fig_3d = plt.figure()
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')

        self.fig_3d.patch.set_facecolor('#333')
        self.ax_3d.set_facecolor('#333')

        self.ax_3d.xaxis.pane.fill = True
        self.ax_3d.yaxis.pane.fill = True
        self.ax_3d.zaxis.pane.fill = True
        self.ax_3d.xaxis.pane.set_facecolor('#333')
        self.ax_3d.yaxis.pane.set_facecolor('#333')
        self.ax_3d.zaxis.pane.set_facecolor('#333')

        self.ax_3d.view_init(elev=20, azim=220)

class TkinterWindow:
    def __init__(self, window, ui, parent):
        self.window = window
        self.parent = parent
        self.ui = ui

        self.is_dragging = False
        self.last_x = 0

        window.title("3D View")
        window.configure(bg="#333")
        window.resizable(False, False)

        right_frame_3d = Frame(self.window, bg="#333")
        right_frame_3d.pack(expand=YES)

        self.canvas_3d = FigureCanvasTkAgg(self.parent.fig_3d, master=right_frame_3d)
        self.canvas_widget_3d = self.canvas_3d.get_tk_widget()
        self.canvas_widget_3d.pack(fill=BOTH, expand=YES)

        self.canvas_widget_3d.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas_widget_3d.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas_widget_3d.bind("<Motion>", self.on_mouse_move)

        self.update_3d_view()

    def on_button_press(self, event):
        self.is_dragging = True
        self.last_x = event.x

    def on_button_release(self, event):
        self.is_dragging = False

    def on_mouse_move(self, event):
        if self.is_dragging:
            delta_x = event.x - self.last_x
            azim = self.parent.ax_3d.azim + delta_x
            self.parent.ax_3d.view_init(elev=20, azim=azim % 360)
            self.canvas_3d.draw()
            self.last_x = event.x

    def update_3d_view(self):
        x = np.arange(self.ui.num_columns_3d)
        y = np.arange(self.ui.num_rows_3d)
        x, y = np.meshgrid(x, y)

        if not self.ui.focused_3d_tab:
            return

        new_values = np.array([[float(self.ui.box_layout.item(i, j).text()) for j in range(self.ui.num_columns_3d)]
                           for i in range(self.ui.num_rows_3d)])

        if self.ui.signed_values:
            for i in range(new_values.shape[0]):
                for j in range(new_values.shape[1]):
                    if new_values[i, j] > 55000:
                        new_values[i, j] = 0

        self.parent.ax_3d.clear()

        surface = self.parent.ax_3d.plot_surface(x, y, new_values, color='#D3D3D3', edgecolor='none')

        self.parent.ax_3d.set_xlabel('X')
        self.parent.ax_3d.set_ylabel('Y')
        self.parent.ax_3d.set_zlabel('Map Value')

        '''if all(entry.get() == "00000" for entry in self.ui.entry_x_widgets[0]) and \
                all(entry.get() == "00000" for entry in self.ui.entry_y_widgets):
            self.ui.ax_3d.set_xticks([])
            self.ui.ax_3d.set_yticks([])
        else:'''

        self.parent.ax_3d.set_xticks(np.arange(0, self.ui.num_columns_3d, 1))
        self.parent.ax_3d.set_yticks(np.arange(0, self.ui.num_rows_3d, 1))

        self.window.after(0, self.canvas_3d.draw)