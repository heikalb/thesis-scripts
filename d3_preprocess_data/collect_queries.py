# —*— coding: utf—8 —*—
"""
Create one file or multiple separate files with target verbs and their context windows are joined.
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


# Given a sentence that may span multiple sentence boundaries, return the 
# sentence containing the target word only and the index of the target word
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
            csv_reader = csv.reader(f, delimiter='\t')
            rows = [r for r in csv_reader]

        curr_stem = filename.split('_')[2]
        print(filename)

        # Process data windows, skip first rows
        for row in rows[1:]:
            # Orthographic processing, get the register of the datum
            left_span = depunctuate(row[2])
            mid_word = apply_correction(depunctuate(row[3]))
            right_span = depunctuate(row[4])
            register = row[0]

            # Fix main columns with multiple words. 
            # Fix cases of main words duplicated in context windows.
            columns = fix_columns(left_span, mid_word, right_span, curr_stem)
            left_span, mid_word, right_context = columns

            # Join context windows, reduce to one sentence
            full_sentence = ' '.join([left_span, mid_word, right_context])
            fixed_sent = to_one_sentence(full_sentence, len(left_span.split()))
            single_sent, target_i = fixed_sent
            save_rows.append([single_sent, mid_word, target_i, register])

        # Option 1: Save data in individual files
        if not all_in_one_file:
            file = f'../d2_data/joined/{filename[:3]}_{curr_stem}_joined.tsv'
            save_file(file, save_rows)
            save_rows.clear()
            rows.clear()

    # Option 2: Save all data in one file
    if all_in_one_file:
        file = '../d2_data/freq_dict_query_results_joined.tsv'
        save_file(file, save_rows)


if __name__ == "__main__":
    query_dir = '../d2_data/query_results_freq_dict/'
    main(query_dir, False)
    exit(0)
