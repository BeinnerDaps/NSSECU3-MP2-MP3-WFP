# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['RBCODLmd.py'],
    pathex=['C:/Users/Bien Rafael/OneDrive/Documents/De Lasalle University/3rd year - TERM 3/NSSECU3/NSSECU3_Git/MP2'],
    binaries=[('tools/RBCmd.exe','.')],
    datas=[('tools', 'tools')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RBCmdOdlParser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
