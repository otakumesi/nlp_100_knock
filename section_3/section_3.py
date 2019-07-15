import gzip
import json
import re
import requests
import pprint

def extract_document_from_json_gz(filename):
    lines = []
    with gzip.open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line)
            lines.append(obj)
    return lines

if __name__ == '__main__':

    docs = extract_document_from_json_gz('./jawiki-country.json.gz')

    # 20
    for doc in docs:
        if doc['title'] == 'イギリス':
            british_doc = doc
    target_lines = british_doc['text'].split('\n')

    # 21
    category_pattern = r'Category:'
    lines_included_category = [(i + 1, t) for i, t in enumerate(target_lines) if re.search(category_pattern, t)]

    # 22
    category_pattern = r'\[\[Category:(.+)\]\]'
    words_included_category = re.findall(category_pattern, british_doc['text'])

    # 23
    section_pattern = '(=+)([^=]+)(=+)\n'
    word_with_count_included_category = [ (fa[1].strip(), len(fa[2])-1) for fa in re.findall(section_pattern, british_doc['text'])]

    # 24
    category_pattern = r'\[\[(ファイル|File):([^]|]+?)(\|.*?)+\]\]'
    words_included_category = list(map(lambda t: t[1], re.findall(category_pattern, british_doc['text'])))

    # 25
    def extract_base_info(text):
        base_info_template_pattern = r'\{\{基礎情報 国\n(.+\n)+\}\}'
        return re.search(base_info_template_pattern, text)[0]

    def extract_media_template_attrs(text):
        info_attr_pattern = r'^\|(.+?)\s*=\s*(.+?)(?:(?=\n\|)|(?=\n$))'
        return re.findall(info_attr_pattern, text, flags=(re.MULTILINE + re.DOTALL))

    # 26
    def delete_emphasis(text):
        return text.replace('"', '').replace("'", '')

    # 27
    def inner_link_to_plain_text(text):
        inner_link_pattern = r"\[\[(.+\|)?(.+?)\]\]"
        return re.sub(inner_link_pattern, r'\2', text)

    # 28
    def remove_markup(text):
        text_deleted_emphasis = delete_emphasis(text)
        text_replaced_inner_link = inner_link_to_plain_text(text_deleted_emphasis)
        text_removed_br = re.sub('<br\s?/>', '', text_replaced_inner_link)
        text_removed_refs = re.sub(r'<ref(.*?)>(\[.+?\])?(.*?)<\/ref>', r'\3', text_removed_br, flags=re.DOTALL)
        text_removed_ref = re.sub(r'<ref .+?\/>', r'', text_removed_refs)
        text_removed_inner_template = re.sub(r'\{\{(.+?\|)*(.+?)\}\}', r'\2', text_removed_ref)
        text_replace_newline = re.sub(r'\n\*+', r' ', text_removed_inner_template)
        return text_replace_newline

    # 29
    url = 'https://ja.wikipedia.org/w/api.php'
    media_attrs = [(attr[0], remove_markup(attr[1])) for attr in extract_media_template_attrs(extract_base_info(british_doc.get('text')))]
    for attr in media_attrs:
        if attr[0] == '国旗画像':
            params = {
                'action': 'query',
                'format': 'json',
                'prop': 'imageinfo',
                'iiprop': 'url',
                'titles': 'File:{}'.format(attr[1])
            }
            res = requests.get(url, params=params)
            image_url = res.json()['query']['pages']['-1']['imageinfo'][0]['descriptionurl']
    pprint.pprint(image_url)
