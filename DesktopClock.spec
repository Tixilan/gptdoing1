# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['desktop_clock/__main__.py'],
    pathex=['.'], binaries=[], datas=[], hiddenimports=[], hookspath=[],
    hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False, optimize=1,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='DesktopClock', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console=False, disable_windowed_traceback=False,
    argv_emulation=False, target_arch=None, codesign_identity=None,
    entitlements_file=None, icon='build/icon.ico',
    version='build/windows_version_info.txt',
)

