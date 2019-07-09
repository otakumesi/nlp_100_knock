if __name__ == "__main__":
    # 00
    word_00 = 'stressed'
    print('00: ', word_00[::-1])

    # 01
    word_01 = 'パタトクカシーー'
    print('01: ', word_01[1::2])

    # 02
    patcar, taxi = 'パトカー', 'タクシー'
    merged_str = [[p, t] for p, t in zip(patcar, taxi)]
    print('02: ', ''.join(sum(merged_str, [])))

    # 03
    sentence_03 = 'Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics.'
    words_03 = sentence_03.replace(',', '').rstrip('.').split(' ')
    print('03: ', [len(w) for w in words_03])

    # 04
    sentence_04 = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
    nums_of_extracting_first_char = [1, 5, 6, 7, 8, 9, 15, 16, 19]
    words_04 = sentence_04.replace('.', '').split(' ')
    words_dict = { (i+1):w for i, w in enumerate(words_04)}
    chars_dict = {}
    for i, w in words_dict.items():
        if i in nums_of_extracting_first_char:
            chars_dict[i] = w[0]
        else:
            chars_dict[i] = w[0:2]
    print('04: ', chars_dict)

    # 05
    def build_n_gram(seq, n = 3):
        return [seq[i] + seq[i + 1] for i, _ in enumerate(seq) if len(seq) > i + 1]

    sentence_05 = 'I am an NLPer'
    words = sentence_05.split(' ')
    chars = list(sentence_05.replace(' ', ''))
    print('05: ', '単語bi-gram', build_n_gram(words))
    print('05: ', '文字bi-gram', build_n_gram(chars))

    # 06
    word_06_1, word_06_2 = 'paraparadise', 'paragraph'
    X = set(build_n_gram(list(word_06_1)))
    Y = set(build_n_gram(list(word_06_2)))
    print('06: ', X | Y)
    print('06: ', X - Y)
    print('06: ', X & Y)
    print('06: ', 'se' in (X & Y))

    # 07

    def gen_sentence_in_ja(x, y, z):
        return "{}時の{}は{}".format(x, y, z)
    print('07: ', gen_sentence_in_ja(12, '気温', 22.4))

    # 08
    def cipher(sentence):
        crypted_sentence_list = []
        for c in sentence:
            if 97 <= ord(c) and ord(c) <= 122:
                crypted_sentence_list.append(chr(219 - ord(c)))
            else:
                crypted_sentence_list.append(c)
        return ''.join(crypted_sentence_list)

    print('08: ', cipher('Hello, World!です。'))
    print('08: ', cipher(cipher('Hello, World!です。')))

    # 09
    def typoglycemia(word):
        if len(word) <= 4:
            return word

        import random
        first, last = word[0], word[-1]
        contents = word[1:-1]
        sorted_contents = ''.join(random.sample(contents, k=len(contents)))
        return first + sorted_contents + last

    sentence_09 = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
    words_09 = sentence_09.split(' ')
    print('09: ', ' '.join([typoglycemia(w) for w in words_09]))
