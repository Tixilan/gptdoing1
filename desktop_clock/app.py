from __future__ import annotations

import ctypes
import tkinter as tk
from datetime import datetime
from typing import Any

from .i18n import format_date, format_time, text
from .settings import ensure_visible_position, load_settings, save_settings


WINDOW_WIDTH = 360
WINDOW_HEIGHT = 160
TRANSPARENT_COLOR = "#010203"
THEMES = {
    "dark": {"background": "#151923", "time": "#F5F7FA", "date": "#A8B0C0", "accent": "#65A7FF"},
    "light": {"background": "#F4F7FB", "time": "#172033", "date": "#5D687B", "accent": "#2575D8"},
}


def enable_windows_dpi_awareness() -> None:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass


def virtual_desktop_bounds(root: tk.Tk) -> tuple[int, int, int, int]:
    try:
        user32 = ctypes.windll.user32
        return (
            user32.GetSystemMetrics(76),
            user32.GetSystemMetrics(77),
            user32.GetSystemMetrics(78),
            user32.GetSystemMetrics(79),
        )
    except (AttributeError, OSError):
        return (0, 0, root.winfo_screenwidth(), root.winfo_screenheight())


def rounded_rectangle(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, radius: int, **kwargs: Any) -> int:
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=24, **kwargs)


class ClockApplication:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.settings = load_settings()
        self.drag_origin: tuple[int, int, int, int] | None = None
        self.update_job: str | None = None

        root.title(text(self.settings["language"], "app_name"))
        root.overrideredirect(True)
        root.configure(bg=TRANSPARENT_COLOR)
        root.resizable(False, False)
        root.attributes("-topmost", self.settings["always_on_top"])
        try:
            root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        except tk.TclError:
            pass

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=TRANSPARENT_COLOR,
            highlightthickness=0,
            borderwidth=0,
        )
        self.canvas.pack()
        self.background_item = rounded_rectangle(self.canvas, 4, 4, WINDOW_WIDTH - 4, WINDOW_HEIGHT - 4, 25)
        self.accent_item = self.canvas.create_rectangle(32, 128, 96, 131, width=0)
        self.time_item = self.canvas.create_text(
            WINDOW_WIDTH // 2,
            65,
            font=("Segoe UI Light", 42),
            anchor="center",
        )
        self.date_item = self.canvas.create_text(
            WINDOW_WIDTH // 2,
            116,
            font=("Segoe UI", 11),
            anchor="center",
        )

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drag)
        self.canvas.bind("<Button-3>", self.show_menu)
        root.bind("<Control-q>", lambda _event: self.close())
        root.protocol("WM_DELETE_WINDOW", self.close)

        self.apply_theme()
        self.place_window()
        self.tick()

    def place_window(self) -> None:
        self.root.update_idletasks()
        saved = self.settings["window"]
        if saved["x"] is None or saved["y"] is None:
            bounds = virtual_desktop_bounds(self.root)
            x = bounds[0] + (bounds[2] - WINDOW_WIDTH) // 2
            y = bounds[1] + (bounds[3] - WINDOW_HEIGHT) // 2
        else:
            x, y = ensure_visible_position(
                saved["x"], saved["y"], WINDOW_WIDTH, WINDOW_HEIGHT, virtual_desktop_bounds(self.root)
            )
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}{x:+d}{y:+d}")

    def tick(self) -> None:
        now = datetime.now()
        self.canvas.itemconfigure(self.time_item, text=format_time(now, self.settings["time_format"]))
        self.canvas.itemconfigure(self.date_item, text=format_date(now, self.settings["language"]))
        self.update_job = self.root.after(200, self.tick)

    def apply_theme(self) -> None:
        palette = THEMES[self.settings["theme"]]
        self.canvas.itemconfigure(self.background_item, fill=palette["background"], outline=palette["background"])
        self.canvas.itemconfigure(self.time_item, fill=palette["time"])
        self.canvas.itemconfigure(self.date_item, fill=palette["date"])
        self.canvas.itemconfigure(self.accent_item, fill=palette["accent"])

    def start_drag(self, event: tk.Event) -> None:
        self.drag_origin = (event.x_root, event.y_root, self.root.winfo_x(), self.root.winfo_y())

    def drag(self, event: tk.Event) -> None:
        if self.drag_origin is None:
            return
        start_x, start_y, window_x, window_y = self.drag_origin
        x = window_x + event.x_root - start_x
        y = window_y + event.y_root - start_y
        self.root.geometry(f"{x:+d}{y:+d}")

    def finish_drag(self, _event: tk.Event) -> None:
        self.drag_origin = None
        self.settings["window"] = {"x": self.root.winfo_x(), "y": self.root.winfo_y()}
        save_settings(self.settings)

    def set_value(self, key: str, value: Any) -> None:
        self.settings[key] = value
        if key == "theme":
            self.apply_theme()
        elif key == "always_on_top":
            self.root.attributes("-topmost", value)
        elif key == "language":
            self.root.title(text(value, "app_name"))
        save_settings(self.settings)
        self.tick_now()

    def tick_now(self) -> None:
        if self.update_job is not None:
            self.root.after_cancel(self.update_job)
        self.tick()

    def reset_position(self) -> None:
        self.settings["window"] = {"x": None, "y": None}
        self.place_window()
        self.settings["window"] = {"x": self.root.winfo_x(), "y": self.root.winfo_y()}
        save_settings(self.settings)

    def show_menu(self, event: tk.Event) -> None:
        language = self.settings["language"]
        menu = tk.Menu(self.root, tearoff=False)

        format_menu = tk.Menu(menu, tearoff=False)
        format_menu.add_command(label=text(language, "format_24h"), command=lambda: self.set_value("time_format", "24h"))
        format_menu.add_command(label=text(language, "format_12h"), command=lambda: self.set_value("time_format", "12h"))
        menu.add_cascade(label=f"{text(language, 'time_format')}  ·  {self.settings['time_format']}", menu=format_menu)

        theme_menu = tk.Menu(menu, tearoff=False)
        theme_menu.add_command(label=text(language, "dark"), command=lambda: self.set_value("theme", "dark"))
        theme_menu.add_command(label=text(language, "light"), command=lambda: self.set_value("theme", "light"))
        menu.add_cascade(label=f"{text(language, 'theme')}  ·  {text(language, self.settings['theme'])}", menu=theme_menu)

        language_menu = tk.Menu(menu, tearoff=False)
        language_menu.add_command(label=text(language, "chinese"), command=lambda: self.set_value("language", "zh-CN"))
        language_menu.add_command(label=text(language, "english"), command=lambda: self.set_value("language", "en"))
        menu.add_cascade(label=text(language, "language"), menu=language_menu)

        top_label = text(language, "always_on_top")
        if self.settings["always_on_top"]:
            top_label = "✓  " + top_label
        menu.add_command(
            label=top_label,
            command=lambda: self.set_value("always_on_top", not self.settings["always_on_top"]),
        )
        menu.add_separator()
        menu.add_command(label=text(language, "reset_position"), command=self.reset_position)
        menu.add_command(label=text(language, "exit"), command=self.close)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def close(self) -> None:
        self.settings["window"] = {"x": self.root.winfo_x(), "y": self.root.winfo_y()}
        save_settings(self.settings)
        if self.update_job is not None:
            self.root.after_cancel(self.update_job)
        self.root.destroy()


def smoke_test() -> None:
    sample = datetime(2026, 11, 25, 13, 5, 9)
    assert format_time(sample, "24h") == "13:05:09"
    assert "2026" in format_date(sample, "en")


def main() -> None:
    enable_windows_dpi_awareness()
    root = tk.Tk()
    ClockApplication(root)
    root.mainloop()

