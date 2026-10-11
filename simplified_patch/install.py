"""Map the Traditional Chinese resources to bundled native Simplified Chinese.

Original archive data stays in place. Replacements are appended; only TOC
entries for the selected files change. A saved original TOC and length allow
exact restoration without copying the 10 GB archive.
"""
import hashlib, json, struct, sys, zlib
from pathlib import Path
from psarc import Psarc

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE / 'vendor'))
from opencc import OpenCC

def records(data):
    assert data[:4] == b'txbL'
    assert struct.unpack_from('<I', data, 8)[0] == len(data)
    count = struct.unpack_from('<I', data, 12)[0]
    hashes = struct.unpack_from('<' + str(count) + 'I', data, 40)
    offsets = struct.unpack_from('<' + str(count) + 'I', data, 40 + count*4)
    start = 40 + count*8
    assert offsets[0] == 0 and list(offsets) == sorted(offsets)
    return {key: data[start+offset:start+(offsets[i+1] if i+1<count else len(data)-start)] for i,(key,offset) in enumerate(zip(hashes,offsets))}

def translate_record(record, converter):
    end = record.index(b'\0', 28)
    original = record[28:end].decode('utf-8')
    translated = converter.convert(original).encode('utf-8')
    # Preserve all glyph lengths, style data and alignment in these DLC records.
    assert len(translated) == end-28
    assert len(converter.convert(original)) == len(original)
    return record[:28] + translated + record[end:]

def make_txb(ct, cs, converter):
    old, native = records(ct), records(cs)
    missing = sorted(old.keys()-native.keys())
    # Preserve the original set of identifiers, including CT-exclusive DLC keys.
    merged = {key: native[key] if key in native else translate_record(old[key],converter) for key in old}
    keys = sorted(merged)
    offsets, payload = [], bytearray()
    for key in keys:
        offsets.append(len(payload))
        payload.extend(merged[key])
    header = bytearray(ct[:40])
    result = header + struct.pack('<' + str(len(keys)) + 'I', *keys) + struct.pack('<' + str(len(keys)) + 'I', *offsets) + payload
    struct.pack_into('<I', result, 8, len(result))
    assert records(result) == merged
    return bytes(result), len(keys)-len(missing), len(missing)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    backup = HERE / 'backup'
    if (backup / 'state.json').exists():
        raise SystemExit('Patch is already installed. Restore it before reinstalling.')
    supported_path = HERE / 'supported.json'
    if supported_path.exists():
        for spec in json.loads(supported_path.read_text(encoding='utf-8')):
            path = ROOT / spec['archive']
            if not path.is_file() or path.stat().st_size != spec['original_size']:
                raise SystemExit('Unsupported or modified game archive: ' + path.name)
            with path.open('rb') as stream:
                header = stream.read(spec['header_size'])
            if digest(header) != spec['original_header_sha256']:
                raise SystemExit('Unsupported archive version: ' + path.name)
    arcs = [Psarc(ROOT/name) for name in ('Gravite2_Chunk0.psarc','Gravite2_Patch_Chunk0.psarc')]
    effective = {name:(arc,i) for arc in arcs for i,name in enumerate(arc.names)}
    converter = OpenCC('t2s')
    jobs, report = [], []
    for arc in arcs:
        replacements = {}
        for i,name in enumerate(arc.names):
            if name.endswith('_CT.txb'):
                ct_arc,ct_i = effective[name]
                cs_arc,cs_i = effective[name.replace('_CT.txb','_CS.txb')]
                data, native_count, converted_count = make_txb(ct_arc.read(ct_i),cs_arc.read(cs_i),converter)
                replacements[i] = data
                report.append(dict(archive=arc.path.name,path=name,native_strings=native_count,converted_strings=converted_count,sha256=digest(data)))
            elif name == 'txb/FontTable2_CT.bin':
                src,j = effective['txb/FontTable2_CS.bin']
                replacements[i] = src.read(j)
                report.append(dict(archive=arc.path.name,path=name,font='native Simplified Chinese',sha256=digest(replacements[i])))
        arc.f.seek(0)
        toc_size = int.from_bytes(arc.f.read(16)[12:16],'big')
        arc.f.seek(0)
        original_header = arc.f.read(toc_size)
        header = bytearray(original_header)
        tail = bytearray()
        original_size = arc.path.stat().st_size
        for i,data in replacements.items():
            e = arc.entries[i]
            old_blocks = (e['size']+arc.block_size-1)//arc.block_size
            new_blocks = (len(data)+arc.block_size-1)//arc.block_size
            assert old_blocks == new_blocks, (arc.path.name,arc.names[i],old_blocks,new_blocks)
            entry_start = 32 + i*30
            header[entry_start+20:entry_start+25] = len(data).to_bytes(5,'big')
            header[entry_start+25:entry_start+30] = (original_size+len(tail)).to_bytes(5,'big')
            for block_no in range(new_blocks):
                raw = data[block_no*arc.block_size:(block_no+1)*arc.block_size]
                compressed = zlib.compress(raw,9)
                block = compressed if len(compressed)<len(raw) else raw
                position = 32+len(arc.entries)*30 + (e['block']+block_no)*2
                header[position:position+2] = (len(block)%arc.block_size).to_bytes(2,'big')
                tail.extend(block)
        jobs.append((arc,replacements,original_header,bytes(header),bytes(tail),original_size))
    if '--check' in sys.argv:
        print('Compatibility check passed. No game files were modified.')
        print('Replacement resources:',sum(len(job[1]) for job in jobs))
        return
    backup.mkdir(exist_ok=True)
    state = []
    for arc,replacements,original_header,header,tail,original_size in jobs:
        (backup/(arc.path.name+'.toc')).write_bytes(original_header)
        state.append(dict(archive=arc.path.name,original_size=original_size,patched_size=original_size+len(tail),original_header_sha256=digest(original_header),patched_header_sha256=digest(header),tail_sha256=digest(tail),header_size=len(header)))
    (backup/'state.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
    completed = []
    try:
        for arc,replacements,original_header,header,tail,original_size in jobs:
            arc.f.close()
            completed.append((arc.path,original_header,original_size))
            with arc.path.open('r+b') as stream:
                stream.seek(original_size); stream.write(tail); stream.flush()
                stream.seek(0); stream.write(header); stream.flush()
            check = Psarc(arc.path)
            for i,expected in replacements.items():
                assert check.read(i) == expected
            assert check.names == arc.names
            for i,(old,new) in enumerate(zip(arc.entries,check.entries)):
                if i not in replacements:
                    assert old == new
                    blocks = (old['size']+arc.block_size-1)//arc.block_size
                    assert arc.blocks[old['block']:old['block']+blocks] == check.blocks[old['block']:old['block']+blocks]
            check.f.close()
            print(arc.path.name, 'verified', len(replacements), 'resources;',len(tail),'bytes appended')
    except BaseException:
        for path,original_header,size in completed:
            with path.open('r+b') as stream:
                stream.seek(0);stream.write(original_header);stream.truncate(size)
        (backup/'state.json').unlink()
        raise
    (HERE/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Installed successfully. Select Traditional Chinese in your emulator.')

if __name__ == '__main__':
    main()
