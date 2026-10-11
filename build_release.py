"""Build a redistributable package from an explicit source allowlist."""
import ast
import hashlib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATCH = ROOT / 'simplified_patch'
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
target = OUT / 'GravityRush2_CUSA04934_SimplifiedChinese_v1.0.zip'
files = ['psarc.py','install.py','restore.py','supported.json','Install.cmd','Restore.cmd','使用说明.md']
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for name in files:
        if name.endswith('.py'):
            ast.parse((PATCH/name).read_text(encoding='utf-8'))
        archive.write(PATCH/name, 'simplified_patch/'+name)
    for path in sorted((PATCH/'vendor').rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            archive.write(path, 'simplified_patch/'+path.relative_to(PATCH).as_posix())
    for name in ('LICENSE','THIRD_PARTY_NOTICES.md'):
        archive.write(ROOT/name,name)
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    assert not any('/backup/' in n or '/inspection/' in n or n.endswith(('.psarc','.pkg','.txb','.ttf','.otf')) for n in archive.namelist())
sha = hashlib.sha256(target.read_bytes()).hexdigest()
target.with_suffix('.sha256.txt').write_text(sha+'  '+target.name+'\n',encoding='ascii')
print(target)
print('SHA256:',sha)
