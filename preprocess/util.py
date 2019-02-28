"""
Apply spell spell correction suggestions to matching words
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
spell_corrections = open('verb_spelling_suggestions_2.txt').read().split('\n')
spell_corrections = [line.split() for line in spell_corrections]
spell_corrections = [l for l in spell_corrections if not (l[0] == '#' or l[0] == '@' or len(l) > 2)]

sentence_punct = ['.', '!', '?']


def apply_correction(target_word):
    target_word_normalized = ''.join([ch for ch in target_word if ch.isalpha()])
    target_word_normalized = target_word_normalized.lower()

    for sp in spell_corrections:
        if sp[0] == target_word_normalized:
            meep = restore_punct(target_word, sp[1])
            return meep

    return target_word


def restore_punct(word_1, word_2):
    if not any(not ch.isalpha() for ch in word_1):
        return word_2

    left_punct = ''
    right_punct = ''
    midpoint = int(len(word_1)/2)

    for ch in word_1[:midpoint]:
        if not ch.isalpha():
            left_punct += ch
        else:
            break

    for ch in word_1[midpoint:]:
        if not ch.isalpha():
            right_punct += ch

    return '{0}{1}{2}'.format(left_punct, word_2, right_punct)


def to_one_sentence(sentence, target_word):
    tokens = sentence.split()
    target_i = tokens.index(target_word)
    new_sent_words = [t for t in tokens]
    right_sent = []
    left_sent = []

    for t in tokens[target_i:]:
        right_sent.append(t)

        if any(punct in t for punct in sentence_punct):
            break

    tokens_ = [t for t in tokens]




    return ' '.join(new_sent_words)

