# —*— coding: utf—8 —*—
"""
Create one file or multiple separate files with target verbs and their context
windows are joined.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import os
import re
from spelling_sub import suggestions


def apply_correction(target_word):
    """
    Apply spelling correction based on spell correction suggestion file.
    :param target_word: word to be spell-corrected
    :return: spell-corrected word
    """
    # Normalize the word
    target_word = target_word.lower()

    # Apply spelling transformations
    for sug in suggestions:
        if re.search(sug, target_word):
            return re.sub(sug, suggestions[sug], target_word)

    return target_word


def to_one_sentence(sentence, target_i):
    """
    Given a sentence that may span multiple sentence boundaries, return the
    sentence containing the target word only and the index of the target word.
    :param sentence: the sentence
    :param target_i: index of the target verb
    :return: pair containing the reduced sentence and index of the target verb
    """
    # Tokenize the sentence
    tokens = sentence.split()

    # Sub-sentence to the left and right of the target verb
    left_sent = []
    right_sent = []

    # Sentence boundary characters
    sentence_punct = ['.', '!', '?']

    # Build the right sub-sentence
    for t in tokens[target_i:]:
        right_sent.append(t)

        if any(punct in t for punct in sentence_punct):
            break

    # Build the left sub-sentence
    i = target_i - 1

    while i >= 0:
        if any(punct in tokens[i] for punct in sentence_punct):
            break

        left_sent.insert(0, tokens[i])
        i -= 1

    # Join the entire sentence containing the target verb
    return ' '.join(left_sent + right_sent), len(left_sent)


def depunctuate(st):
    """
    Remove punctuation from a string.
    :param st: the string
    :return: depuntuated string
    """
    # Normalize the string
    st = st.strip().lower().split()
    new_sent = []

    for w in st:
        # Remove non-letters/numbers
        new_word = [ch for ch in w if ch.isalnum()]

        # Exclude purely punctuation words
        if new_word:
            new_sent.append(''.join(new_word))

    return ' '.join(new_sent)


def fix_columns(left, mid, right, stem):
    """
    Fix errors related to sentence/word columns in the dataset.
    :param left: the left column
    :param mid: the middle word column
    :param right: the right column
    :param stem: the stem of the target verb
    :return: the fixed columns
    """
    # Tokenize the middle column if there are multiple words in it
    mid_words = mid.split()

    # If if there are multiple words in middle column, fix it fix occurrences
    # of repeated words in the surrounding columns
    if len(mid_words) > 1:
        if left.endswith(mid):
            left = left.replace(mid, '').strip()
        elif right.startswith(mid):
            right = right.replace(mid, '').strip()

        if [w for w in mid_words if stem in w]:
            mid = [w for w in mid_words if stem in w][0]
        else:
            mid = mid_words[0]

    # Return fixed columns
    return left, mid, right


def save_file(fname, data_list):
    """
    Save processed data.
    :param fname: filename to save in
    :param data_list: processed dataset
    """
    with open(fname, 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')

        for r in data_list:
            csv_writer.writerow(r)


def main():
    """
    Main method.
    """
    save_rows = []
    data_dir = '../d2_data/query_results_freq_dict/'

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

            # Save data in individual files by verb
            file = f'../d2_data/joined/{filename[:3]}_{curr_stem}_joined.tsv'
            save_file(file, save_rows)


if __name__ == "__main__":
    main()
    exit(0)
