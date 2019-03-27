# —*— coding: utf—8 —*—
"""
Gather all query results (verbs + context window) from different verbs into one file
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv

spell_corrections = open('verb_spelling_suggestions_2.txt').read().split('\n')
spell_corrections = [line.split() for line in spell_corrections]
spell_corrections = [l for l in spell_corrections if not (l[0] == '#' or l[0] == '@' or len(l) < 2)]
sentence_punct = ['.', '!', '?']

window_corrections = open('window_corrections.tsv').read().split('\n')
window_corrections = [wc.split('\t') for wc in window_corrections]


# Apply spelling correction based on spell correction suggestion file
def apply_correction(target_word):
    target_word_normalized = ''.join([ch for ch in target_word if ch.isalpha()])
    target_word_normalized = target_word_normalized.lower()

    for sp in spell_corrections:
        if sp[0] == target_word_normalized:
            return sp[1]

    return target_word


# Helper method for apply_correction(). Restores punctuation back into a word
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


# Given a sentence that may span multiple sentence boundaries, return the sentence containing the target word only
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

    return ' '.join(left_sent + right_sent), len(left_sent)


# Remove punctuation from a string
def depunctuate(st):
    st = st.split()
    new_sent = []

    for w in st:
        new_word = [ch for ch in w if ch.isalnum()]

        if new_word:
            new_sent.append(''.join(new_word))

    return ' '.join(new_sent)


def window_correction(orig_window):
    for wc in window_corrections:
        if wc[1] == orig_window[1]:
            ret = wc[0:2] + wc[5:8]
            window_corrections.remove(wc)
            return ret

    return orig_window


def main():
    rows = []
    
    for i in range(20):
        # Open file
        with open('../2_data/query_results/tnc_query_result_{0}.tsv'.format(i)) as f:
            csv_reader = csv.reader(f, delimiter='\t')

            first_row = True
            for row in csv_reader:
                # Skip first row header of CSV
                if first_row:
                    first_row = False
                    continue

                # Apply correction to certain 2_data windows
                if window_corrections:
                    row = window_correction(row)

                # Spell correct target verb
                main_word = apply_correction(depunctuate(row[3]))
                left_context = depunctuate(row[2])
                right_context = depunctuate(row[4])

                # Join context windows and target verb, remove punctuation
                full_sentence = ' '.join([left_context, main_word, right_context])
                # Reduce context window to one sentence, get  new index of target verb
                single_sent = to_one_sentence(full_sentence, len(left_context.split()))
                # Save processed context window
                rows.append([single_sent[0], main_word, single_sent[1]])

    # Save data
    with open('../2_data/query_results_all_joined_sents.tsv', 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        for r in rows:
            csv_writer.writerow(r)


if __name__ == "__main__":
    main()
    exit(0)