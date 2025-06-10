# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\faq_system.py'],
    pathex=[],
    binaries=[],
    datas=[('faq_database.db', '.')],
    hiddenimports=[
        'PyQt5.sip', 
        'pandas', 
        'pandas._libs.tslibs', 
        'pandas._libs.interval', 
        'pandas._libs.writers',
        'pandas._libs.json',
        'pandas._libs.ops',
        'pandas._libs.parsers',
        'openpyxl',
        'openpyxl.styles',
        'xlrd'
    ],
    hookspath=['.'],
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
    a.binaries,
    a.datas,
    [],
    name='faq_system',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 暂时开启控制台以便调试
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
