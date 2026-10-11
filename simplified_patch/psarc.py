import struct, zlib
from pathlib import Path

class Psarc:
    def __init__(self, path):
        self.path = Path(path)
        self.f = self.path.open('rb')
        header = self.f.read(32)
        magic, version, compression, toc_size, entry_size, count, self.block_size, flags = struct.unpack('>4sI4sIIIII', header)
        if magic != b'PSAR' or compression != b'zlib' or entry_size != 30:
            raise ValueError(header.hex())
        toc = self.f.read(toc_size - 32)
        self.entries = []
        for i in range(count):
            e = toc[i*30:(i+1)*30]
            self.entries.append(dict(hash=e[:16].hex(), block=int.from_bytes(e[16:20],'big'), size=int.from_bytes(e[20:25],'big'), offset=int.from_bytes(e[25:30],'big')))
        width = (self.block_size.bit_length()-1 + 7)//8
        self.blocks = [int.from_bytes(toc[i:i+width],'big') for i in range(count*30,len(toc),width)]
        names = self.read(0).decode('utf-8').splitlines()
        if len(names) != count-1:
            raise ValueError((len(names), count))
        self.names = ['<manifest>'] + names

    def read(self, index):
        e = self.entries[index]
        self.f.seek(e['offset'])
        out = bytearray()
        block = e['block']
        while len(out) < e['size']:
            size = self.blocks[block] or self.block_size
            raw = self.f.read(size)
            expected = min(self.block_size, e['size']-len(out))
            if size == expected:
                decoded = raw
            else:
                decoded = zlib.decompress(raw)
            if len(decoded) != expected:
                raise ValueError((index, block, len(decoded), expected))
            out.extend(decoded)
            block += 1
        return bytes(out)

if __name__ == '__main__':
    import json
    root = Path(__file__).resolve().parent.parent
    output = Path(__file__).resolve().parent / 'inspection'
    output.mkdir(exist_ok=True)
    for path in root.glob('*.psarc'):
        arc = Psarc(path)
        (output/(path.stem+'.json')).write_text(json.dumps([dict(name=n, **e) for n,e in zip(arc.names,arc.entries)],ensure_ascii=False,indent=2),encoding='utf-8')
        candidates = [(i,n,arc.entries[i]['size']) for i,n in enumerate(arc.names) if any(s in n.lower() for s in ('chinese','china','cht','chs','text','font','locale','lang','message','string'))]
        print(path.name, len(arc.names), 'entries', len(candidates), 'candidates')
        print(*candidates[:100],sep='\n')
