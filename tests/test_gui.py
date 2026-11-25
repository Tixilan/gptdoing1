"""Run with CLOCK_GUI_TESTS=1 on Windows with a complete Tcl/Tk runtime."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from desktop_clock.settings import load_settings, save_settings


@unittest.skipUnless(os.environ.get("CLOCK_GUI_TESTS") == "1", "Windows GUI integration opt-in")
class GuiTests(unittest.TestCase):
    def test_window_controls_persist_and_negative_move_is_absolute(self):
        import tkinter as tk
        from desktop_clock.app import ClockApplication
        from desktop_clock.displays import move_window

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            with patch("desktop_clock.app.load_settings", side_effect=lambda: load_settings(path)), \
                 patch("desktop_clock.app.save_settings", side_effect=lambda value: save_settings(value, path)):
                root = tk.Tk()
                try:
                    app = ClockApplication(root)
                    root.update()
                    self.assertTrue(root.winfo_viewable())
                    for key, value in (("theme", "light"), ("language", "en"),
                                       ("time_format", "12h"), ("always_on_top", False)):
                        app.set_value(key, value)
                    root.update()
                    self.assertEqual(app.canvas.itemcget(app.background_item, "fill"), "#F4F7FB")
                    self.assertIn(load_settings(path)["language"], {"en"})
                    self.assertEqual(load_settings(path)["time_format"], "12h")
                    self.assertFalse(bool(root.attributes("-topmost")))
                    move_window(root, -100, 120)
                    root.update()
                    self.assertEqual((root.winfo_x(), root.winfo_y()), (-100, 120))
                    app.close()
                    self.assertEqual(load_settings(path)["window"], {"x": -100, "y": 120})
                    root = tk.Tk()
                    app = ClockApplication(root)
                    root.update()
                    self.assertTrue(root.winfo_viewable())
                    self.assertEqual(app.settings["theme"], "light")
                    self.assertEqual((root.winfo_x(), root.winfo_y()), (-100, 120))
                finally:
                    try:
                        root.destroy()
                    except tk.TclError:
                        pass
