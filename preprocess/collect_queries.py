# —*— coding: utf—8 —*—
"""
Gather all query results (verbs + context window) from different verbs into one file
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import sys
sys.path.append('../../')
import preprocess.util as util


def main():
    rows = []
    
    for i in range(20):
        with open('../data/query_results_/tnc_query_result_{0}.tsv'.format(i)) as f:
            csv_reader = csv.reader(f, delimiter='\t')
            first_row = True

            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue

                main_word = util.apply_correction(row[3])
                before_context_size = len(row[2].split(' '))
                full_sentence = ' '.join([row[2], main_word, row[4]])
                full_sentence = util.to_one_sentence(full_sentence, before_context_size)
                rows.append([full_sentence, main_word, before_context_size])

    with open('../data/query_results_all_joined_sents_.tsv', 'w') as f:
        csv_writer = csv.writer(f, delimiter='\t')

        for r in rows:
            csv_writer.writerow(r)


if __name__ == "__main__":
    main()
    exit(0)