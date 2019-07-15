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
            if bool(morph_dict_list):
                sentence_list.append(morph_dict_list)
                morph_dict_list = []
            continue

        if not re.search(r'^(　|。|、)', line):
            morph_dict_list.append(build_morphe_dict(line))
    return sentence_list

sentence_list = build_sentence_list(build_mecab_lines(read_mecab_file(MECAB_FILE_PATH)))
print(sentence_list)
