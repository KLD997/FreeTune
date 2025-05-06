from PyQt6.QtWidgets import QMessageBox

class DialogManager:
    def __init__(self, ui):
        self.ui = ui

    def open_dialog(self, dialog):
        dialog.finished.connect(lambda: self.on_dialog_closed(dialog))

        dialog.exec()  # Show the dialog

    def on_dialog_closed(self, dialog):
        if self.ui.dialog_terminate:
            if self.ui.potential_map_added:
                self.ui.potential_map_added = False
            QMessageBox.information(self.ui, "Info", "Dialog terminated.")
        dialog.close()
        self.ui.dialog_terminate = True