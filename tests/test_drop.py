import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from desktop_clock.app import ClockApplication
from desktop_clock.settings import load_settings, save_settings


class WindowState:
    x, y = 2200, 100
    def winfo_x(self):
        return self.x
    def winfo_y(self):
        return self.y


class DropTests(unittest.TestCase):
    def test_drop_in_monitor_gap_persists_recovered_position(self):
        app = ClockApplication.__new__(ClockApplication)
        app.root = WindowState()
        app.settings = {}
        def move(root, x, y):
            root.x, root.y = x, y
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'settings.json'
            with patch('desktop_clock.app.monitor_work_areas', return_value=[(0, 0, 1920, 1080), (1920, 1080, 1920, 1080)]), \
                 patch('desktop_clock.app.move_window', side_effect=move), \
                 patch('desktop_clock.app.save_settings', side_effect=lambda value: save_settings(value, path)):
                app.finish_drag(None)
            self.assertEqual(load_settings(path)['window'], {'x': 1560, 'y': 100})
