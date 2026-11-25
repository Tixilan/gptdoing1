"""Windows monitor enumeration and absolute positioning, including negative coordinates."""
import ctypes
from ctypes import wintypes


def monitor_work_areas(root):
    class MonitorInfo(ctypes.Structure):
        _fields_ = [("size", wintypes.DWORD), ("monitor", wintypes.RECT),
                    ("work", wintypes.RECT), ("flags", wintypes.DWORD)]

    result = []
    try:
        user32 = ctypes.windll.user32
        callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HANDLE, wintypes.HDC,
                                          ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)
        user32.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MonitorInfo)]

        def collect(handle, _dc, _rect, _data):
            info = MonitorInfo()
            info.size = ctypes.sizeof(info)
            if user32.GetMonitorInfoW(handle, ctypes.byref(info)):
                r = info.work
                result.append((bool(info.flags & 1), (r.left, r.top, r.right - r.left, r.bottom - r.top)))
            return True

        user32.EnumDisplayMonitors(None, None, callback_type(collect), 0)
    except (AttributeError, OSError):
        pass
    result.sort(key=lambda item: not item[0])
    return [area for _primary, area in result] or [(0, 0, root.winfo_screenwidth(), root.winfo_screenheight())]


def move_window(root, x, y):
    root.update_idletasks()
    try:
        user32 = ctypes.windll.user32
        user32.GetParent.argtypes = [wintypes.HWND]
        user32.GetParent.restype = wintypes.HWND
        user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int,
                                      ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
        handle = user32.GetParent(root.winfo_id()) or root.winfo_id()
        if not user32.SetWindowPos(handle, None, x, y, 0, 0, 0x0001 | 0x0004 | 0x0010):
            raise OSError("SetWindowPos failed")
    except AttributeError:
        root.geometry(f"{x:+d}{y:+d}")
