# —*— coding: utf—8 —*—
"""
Gather all the verbs (only) from the various query result files
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv


def main():
    words = []
    
    for i in range(20):
        with open('../1_data/query_results/tnc_query_result_{0}.tsv'.format(i)) as f:
            csv_reader = csv.reader(f, delimiter='\t')
            first_row = True

            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue

                if len(row[3].split()) > 1:
                    curr_word = ''.join(ch.lower() for ch in row[3].split()[1] if ch.isalpha())
                else:
                    curr_word = ''.join(ch.lower() for ch in row[3] if ch.isalpha())
                # curr_word = row[3]
                words.append(curr_word)
                print(curr_word)
                
    save_file = open('../1_data/all_verbs.txt', 'w')
    save_file.write('\n'.join(words))
    save_file.close()


if __name__ == "__main__":
    main()
    exit(0)
