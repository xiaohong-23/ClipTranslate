# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['F:\\Desktop\\Pyproject\\ClipTranslate\\ClipTranslate.py'],
    pathex=[],
    binaries=[('F:\\Mincoda\\Library\\bin\\tcl86t.dll', '.'), ('F:\\Mincoda\\Library\\bin\\tk86t.dll', '.'), ('F:\\Mincoda\\Library\\bin\\ffi.dll', '.'), ('F:\\Mincoda\\Library\\bin\\liblzma.dll', '.'), ('F:\\Mincoda\\Library\\bin\\libbz2.dll', '.'), ('F:\\Mincoda\\Library\\bin\\zlib.dll', '.')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ClipTranslate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['F:\\Desktop\\Pyproject\\ClipTranslate\\resource\\logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ClipTranslate',
)
