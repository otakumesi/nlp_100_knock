import re

# 30
MECAB_FILE_PATH = './neko.txt.mecab'

def read_mecab_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return text

def build_mecab_lines(mecab_text):
    return [line for line in mecab_text.split('\n')]

def build_morphe_dict(line):
    match = re.search('(.+?)\t+(.+)', line)
    name, morph_raw_list = match.group(1, 2)
    morph_list = morph_raw_list.split(',')

    return {
        'surface': name,
        'base': morph_list[6],
        'pos': morph_list[0],
        'pos1': morph_list[1]
    }

def build_sentence_list(mecab_lines):
    sentence_list = []
    morph_dict_list = []
    for line in mecab_lines:
        if not line:
            continue

        if line.startswith('EOS'):
            if morph_dict_list:
                sentence_list.append(morph_dict_list)
                morph_dict_list = []
            continue

        morph_dict_list.append(build_morphe_dict(line))
    return sentence_list

sentence_list = build_sentence_list(build_mecab_lines(read_mecab_file(MECAB_FILE_PATH)))

# 31
words = sum(sentence_list, [])
verbs = [w for w in words if w['pos'] == '動詞']
verb_surfaces = [v['surface'] for v in verbs]

# 32
verb_bases = [v['base'] for v in verbs]

# 33
nouns = [w for w in words if w['pos'] == '名詞']
sahen_cones = [n for n in nouns if n['pos1'] == 'サ変接続']

# 34
def detect_nouns_connected_by_no(words):
    nouns = []
    for i in range(0, len(words) - 2):
        left, middle, right = words[i:(i+3)]
        if middle['surface'] == 'の' and all([w['pos'] == '名詞' for w in [left, right]]):
            nouns.extend([left, right])
    return nouns

nouns_connected_by_no = detect_nouns_connected_by_no(words)

# 35
def detect_linked_nouns(words):
    linked_nouns = []
    linked_noun = []
    for word in words:
        if word['pos'] == '名詞':
            linked_noun.append(word)
            continue

        if linked_noun:
            linked_nouns.append(linked_noun[:])
            linked_noun = []
    return linked_nouns

linked_nouns = sum([detect_linked_nouns(words) for words in sentence_list], [])
