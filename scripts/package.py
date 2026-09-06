#!/usr/bin/env python3
"""Create a deterministic, offline-ready zip in dist/."""
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'scripts/validate.py'),'--rebuild'],cwd=root,check=True)
destination=root/'dist/icons.zip'
destination.parent.mkdir(exist_ok=True)
files=[root/'README.md',root/'CONTRIBUTING.md',root/'manifest.json',root/'index.html',root/'THIRD_PARTY_NOTICES.md']
for directory in ('icons','variants','catalog','docs','examples','src','scripts'):
    files.extend(path for path in (root/directory).rglob('*') if path.is_file() and '__pycache__' not in path.parts and path.name!='.DS_Store')
with ZipFile(destination,'w',compression=ZIP_DEFLATED,compresslevel=9) as archive:
    for path in sorted(files):
        info=ZipInfo('icons/'+str(path.relative_to(root)),date_time=(2026,1,1,0,0,0))
        info.compress_type=ZIP_DEFLATED
        info.external_attr=0o100644 << 16
        archive.writestr(info,path.read_bytes())
print(destination)
