# —*— coding: utf—8 —*—
"""
Gather all query results (verbs + context window) from different verbs into one file
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import os
import re
from spelling_sub import suggestions

sentence_punct = ['.', '!', '?']


# Apply spelling correction based on spell correction suggestion file
def apply_correction(target_word):
    target_word = target_word.lower()

    for sug in suggestions:
        if re.search(sug, target_word):
            return re.sub(sug, suggestions[sug], target_word)

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
    st = st.strip().lower().split()
    new_sent = []

    for w in st:
        new_word = [ch for ch in w if ch.isalnum()]

        if new_word:
            new_sent.append(''.join(new_word))

    return ' '.join(new_sent)


def main():
    save_rows = []
    data_dir = '../d2_data/query_results_freq_dict/'
    filenames = os.listdir(data_dir)
    filenames.sort()

    for filename in filenames:
        # Get data windows
        file = open(os.path.join(data_dir, filename), 'r')
        csv_reader = csv.reader(file, delimiter='\t')
        rows = [r for r in csv_reader]
        file.close()
        curr_stem = filename.split('_')[2]
        print(filename)

        # Process data windows, skip first rows
        for row in rows[1:]:
            # Spell correct target verb, remove punctuations
            main_word = apply_correction(depunctuate(row[3]))
            left_context = depunctuate(row[2])
            right_context = depunctuate(row[4])

            # When there are multiple words in the target word column, save the word with the correct stem
            target_column = main_word.split()
            if len(target_column) > 1:
                if left_context.endswith(main_word):
                    left_context = left_context.replace(main_word, '').strip()
                elif right_context.startswith(main_word):
                    right_context = right_context.replace(main_word, '').strip()

                if [w for w in target_column if curr_stem in w]:
                    main_word = [w for w in target_column if curr_stem in w][0]
                else:
                    main_word = target_column[0]

            # Join context windows, reduce to one sentence
            full_sentence = ' '.join([left_context, main_word, right_context])
            single_sent = to_one_sentence(full_sentence, len(left_context.split()))
            save_rows.append([single_sent[0], main_word, single_sent[1]])

    # Save data
    with open('../d2_data/freq_dict_query_results_all_joined_sents.tsv', 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        for r in save_rows:
            csv_writer.writerow(r)


if __name__ == "__main__":
    main()
    exit(0)