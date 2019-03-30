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


def fix_columns(left, mid, right, stem):
    mid_words = mid.split()

    if len(mid_words) > 1:
        if left.endswith(mid):
            left = left.replace(mid, '').strip()
        elif right.startswith(mid):
            right = right.replace(mid, '').strip()

        if [w for w in mid_words if stem in w]:
            mid = [w for w in mid_words if stem in w][0]
        else:
            mid = mid_words[0]

    return left, mid, right


def save_file(fname, data_list):
    with open(fname, 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')
        for r in data_list:
            csv_writer.writerow(r)


def main(data_dir, all_in_one_file=False):
    save_rows = []
    filenames = os.listdir(data_dir)
    filenames.sort()

    for filename in filenames:
        # Get data windows
        with open(os.path.join(data_dir, filename), 'r') as f:
            f = open(os.path.join(data_dir, filename), 'r')
            csv_reader = csv.reader(f, delimiter='\t')
            rows = [r for r in csv_reader]

        curr_stem = filename.split('_')[2]
        print(filename)

        # Process data windows, skip first rows
        for row in rows[1:]:
            # Spell correct target verb, remove punctuations
            main_word = apply_correction(depunctuate(row[3]))
            left_context = depunctuate(row[2])
            right_context = depunctuate(row[4])

            # Fix main columns with multiple words. Fix cases of main words duplicated in context windows.
            left_context, main_word, right_context = fix_columns(left_context, main_word, right_context, curr_stem)

            # Join context windows, reduce to one sentence
            full_sentence = ' '.join([left_context, main_word, right_context])
            single_sent = to_one_sentence(full_sentence, len(left_context.split()))
            save_rows.append([single_sent[0], main_word, single_sent[1]])

        if not all_in_one_file:
            # Save data in individual files
            save_file('../d2_data/joined/{0}_{1}_{2}.tsv'.format(filename[:3], curr_stem, 'joined', save_rows))
            save_rows.clear()
            rows.clear()

    # Save all data in one file
    save_file('../d2_data/freq_dict_query_results_joined.tsv', save_rows)


if __name__ == "__main__":
    query_dir = '../d2_data/query_results_freq_dict/'
    main(query_dir, False)
    exit(0)
