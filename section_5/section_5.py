import re

MECAB_FILE_PATH = './neko.txt.cabocha'

def read_mecab_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def build_mecab_sentence_lines(mecab_text):
    return [sentence.split('\n') for sentence in mecab_text.split('EOS') if not sentence == '\n']

def build_morphe(line):
    match = re.search('(.+?)\t+(.+)', line)
    name, morph_raw_list = match.group(1, 2)
    morph_list = morph_raw_list.split(',')

    return Morph(name, morph_list[6], morph_list[0], morph_list[1])

def update_chunk_list(line, chunks):
    src, dst = build_chunk_parts(line)
    if dst == -1:
        return chunks + [Chunk(None, init_src=src)]

    for chunk in chunks:
        if chunk.is_same_dst(dst):
            chunk.add_src(src)
            return chunks

    return chunks + [Chunk(dst, init_src=src)]

def build_chunk_parts(line):
    match = re.search('^\*\s(\d+)\s(-?\d+)D (\d+)/(\d+) (.+)$', line)
    return [int(m) for m in match.group(1, 2)]

def build_sentence_list(mecab_sentence_lines):
    from functools import reduce
    sentence_morph_list, sentence_chunk_list = [], []
    for sentence in mecab_sentence_lines:
        chunk_list = []
        for line in sentence:
            if not line:
                continue

            if line.startswith('* '):
                chunk_list = update_chunk_list(line, chunk_list)
                continue

            chunk_list[-1].add_morph(build_morphe(line))

        sentence_morph_list.append(reduce(lambda acc, c: c.morphs + acc, chunk_list, []))
        sentence_chunk_list.append(chunk_list)
    return sentence_morph_list, sentence_chunk_list

class Morph:
    def __init__(self, surface, base, pos, pos1):
        self._surface = surface
        self._base = base
        self._pos = pos
        self._pos1 = pos1

    @property
    def surface(self):
        return self._surface

    @property
    def base(self):
        return self._base

    @property
    def pos(self):
        return self._pos

    @property
    def pos1(self):
        return self._pos1

class Chunk:
    def __init__(self, dst, init_src=None):
        self._morphs = []
        self._dst = dst
        self._srcs = []
        if init_src:
            self.add_src(init_src)

    @property
    def morphs(self):
        return self._morphs

    @property
    def dst(self):
        return self._dst

    @property
    def srcs(self):
        return self._srcs

    def get_dst_clauses(self):
        return '\t'.join([m.surface for m in self.morphs])

    def add_morph(self, val):
        self._morphs.append(val)

    def is_same_dst(self, val):
        if self._dst is None:
            return False

        return self._dst == val

    def add_src(self, val):
        self._srcs.append(val)

# 40
sentence_morph_list, sentence_chunk_list = build_sentence_list(build_mecab_sentence_lines(read_mecab_file(MECAB_FILE_PATH)))
# print([m.pos for m in sentence_morph_list[2]])

# 41
# print([([m.surface for m in c.morphs], c.dst, c.srcs) for c in sentence_chunk_list[7]])

# 42
for sentence in sentence_chunk_list:
    for chunk in sentence:
        if chunk.dst is not None:
            print([c.morphs for c in sentence])
            print([m.surface for m in sum([c.morphs for c in sentence], [])], chunk.dst, chunk.srcs)
            src_chunks = [c for c in [sentence[s] for s in chunk.srcs]]
            print('{}\t{}'.format(chunk.get_dst_clauses(), '\t'.join([c.get_dst_clauses() for c in src_chunks])))

