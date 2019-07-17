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

# 36
def get_freqs_of_word(words):
    freqs = {}
    for word in words:
        freqs[word['surface']] = freqs.get(word['surface'], 0) + 1
    return freqs

freqs = get_freqs_of_word(words)

word_surfaces = list(set([w['surface'] for w in words if not w['pos'] == '記号']))
word_sorted_by_freqs = sorted(word_surfaces, key=lambda w: freqs[w], reverse=True)

# 37
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Meirio', 'Noto Sans CJK JP']
top_word_freqs = [freqs[w] for w in word_sorted_by_freqs[:11]]
# plt.bar(range(1, len(top_word_freqs) + 1), top_word_freqs, tick_label=word_sorted_by_freqs[:11])
# plt.xlabel('単語')
# plt.ylabel('出現頻度')
# plt.show()

# 38
# plt.hist(list(freqs.values()), bins=10, log=True)
# plt.xlabel('単語の出現頻度')
# plt.ylabel('種類数')
# plt.show()

# 39
freq_ranks = sorted(freqs.values(), reverse=True)
plt.plot([i + 1 for i, v in enumerate(freq_ranks)], freq_ranks)
plt.yscale('log')
plt.xscale('log')
plt.xlabel('単語の出現頻度順位')
plt.ylabel('単語の出現頻度')
plt.show()
