import sys
import os

class Potential_maps_manager:
    def __init__(self, ui):
        self.ui = ui

    def find_potential_maps(self):
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))

        from find_maps import find_potential_maps

        self.ui.potential_maps_start, self.ui.potential_maps_end = find_potential_maps(list(self.ui.unpacked))

        for i in range(len(self.ui.potential_maps_start)):
            self.ui.potential_maps_names.append(f"Potential Map {i}")