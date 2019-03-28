# —*— coding: utf—8 —*—
"""
Gather all query results (verbs + context window) from different verbs into one file
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import os
from spelling_sub import suggestions


# Apply spelling correction based on spell correction suggestion file
def apply_correction(target_word):
    target_word_normalized = target_word.lower()

    for sp in suggestions:
        if sp[0] == target_word_normalized:
            return sp[1]

    return target_word


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


def main():
    rows = []
    data_dir = '../d2_data/query_results_freq_dict/'
    for filename in os.listdir(data_dir):

        file = open(os.path.join(data_dir, filename), 'r')
        csv_reader = csv.writer(file, delimiter='\t')

        first_row = True

        for row in csv_reader:
            # Skip first row header of CSV
            if first_row:
                first_row = False
                continue

            # Spell correct target verb, remove punctuations
            main_word = apply_correction(depunctuate(row[3]))
            left_context = depunctuate(row[2])
            right_context = depunctuate(row[4])
            # Join context windows and target verb, remove punctuation
            full_sentence = ' '.join([left_context, main_word, right_context])
            # Reduce context window to one sentence, get  new index of target verb
            single_sent = to_one_sentence(full_sentence, len(left_context.split()))
            # Save processed context window
            rows.append([single_sent[0], main_word, single_sent[1]])

        file.close()

    # Save data
    with open('../d2_data/query_results_all_joined_sents.tsv', 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        for r in rows:
            csv_writer.writerow(r)


if __name__ == "__main__":
    main()
    exit(0)