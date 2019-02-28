"""
Functions for preprocessing queries
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
spell_corrections = open('verb_spelling_suggestions_2.txt').read().split('\n')
spell_corrections = [line.split() for line in spell_corrections]
spell_corrections = [l for l in spell_corrections if not (l[0] == '#' or l[0] == '@' or len(l) > 2)]
sentence_punct = ['.', '!', '?']


"""
Apply spelling correction based on spell correction suggestion file
"""
def apply_correction(target_word):
    target_word_normalized = ''.join([ch for ch in target_word if ch.isalpha()])
    target_word_normalized = target_word_normalized.lower()

    for sp in spell_corrections:
        if sp[0] == target_word_normalized:
            meep = restore_punct(target_word, sp[1])
            return meep

    return target_word


"""
Helper method for apply_correction(). Restores punctuation back into a word
"""
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


"""
Given a sentence that may span multiple sentence boundaries, return the sentence containing the target word only
"""
def to_one_sentence(sentence, target_i):
    tokens = sentence.split()
    right_sent = []
    left_sent = []

    for t in tokens[target_i:]:
        right_sent.append(t)

        if any(punct in t for punct in sentence_punct):
            break

    i = target_i - 1

    while i >= 0:
        if any(punct in tokens[i] for punct in sentence_punct):
            break

        left_sent.insert(0, tokens[i])

        i -= 1

    return ' '.join(left_sent + right_sent)

