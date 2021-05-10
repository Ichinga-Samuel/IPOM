# -*- mode: python ; coding: utf-8 -*-
import importlib
from pathlib import Path


package_imports = [['qtmodern', ['resources/frameless.qss', 'resources/style.qss']]]

added_file = [('assets\images\*.jpg', 'assets/images'), ('assets\icons\*.png', 'assets\icons'), ('stylesheets\*.qss', 'stylesheets')]
for package, files in package_imports:
    proot = Path(importlib.import_module(package).__file__).parent
    added_file.extend((proot / f, package) for f in files)

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Users\Onyedikachi Oti\\PycharmProjects\\IPOM GUI'],
             binaries=[],
             datas=added_file,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Integrated Palm Oil Extracting Machine Designer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
