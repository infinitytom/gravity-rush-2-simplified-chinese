import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
backup = HERE/'backup'
state_path = backup/'state.json'
if not state_path.exists():
    raise SystemExit('No installed patch was found.')
state = json.loads(state_path.read_text(encoding='utf-8'))
jobs = []
for item in state:
    path = ROOT/item['archive']
    original = (backup/(item['archive']+'.toc')).read_bytes()
    assert hashlib.sha256(original).hexdigest() == item['original_header_sha256']
    assert path.stat().st_size == item['patched_size'], 'Archive changed after patch installation.'
    with path.open('rb') as stream:
        header = stream.read(item['header_size'])
        assert hashlib.sha256(header).hexdigest() == item['patched_header_sha256'], 'Archive header changed.'
        stream.seek(item['original_size'])
        assert hashlib.sha256(stream.read()).hexdigest() == item['tail_sha256'], 'Appended resources changed.'
    jobs.append((path,original,item['original_size']))
for path,original,size in jobs:
    with path.open('r+b') as stream:
        stream.seek(0);stream.write(original);stream.truncate(size)
    print('Restored:',path.name)
state_path.replace(backup/'restored-state.json')
