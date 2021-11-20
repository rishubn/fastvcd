from bisect import bisect_right
class Signal:
    def __init__(self) -> None:
        self.indices = []
        self.data = []

    def add(self, i, d):
        self.indices.append(i)
        self.data.append(d)
    
    def __getitem__(self, i):
        x = bisect_right(self.indices, i)
        return self.data[x-1]

def scope_str(heir):
    return '.'.join(heir)

def parse_vcd(f):
    signals = {"id": {}, "name":{}}
    heir = []
    t = 0
    with open(f, 'r') as vcd:
        for line in vcd:
            if "$var" in line:
                l = line.split(" ")
                s = Signal()
                sc = scope_str(heir)
                if l[3] in signals["id"]:
                    signals["name"][f'{sc}.{l[4]}'] = signals["id"][l[3]]
                else:
                    signals["id"][l[3]] = s
                    signals["name"][f'{sc}.{l[4]}'] = s
            elif "$scope" in line:
                l = line.split(" ")
                heir.append(l[2])
            elif "$upscope" in line:
                heir.pop()
            elif line[0] == '#':
                t = int(line[1:].strip())
            elif line[0] == '$':
                pass
            else:
                l = list(line)
                id = l[1]
                x = int(l[0])
                signals['id'][id].add(t, x)
    return signals


signals = parse_vcd('test.vcd')
print(signals)