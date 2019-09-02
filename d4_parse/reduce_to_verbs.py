"""
Reduce the file of parses to parses of target verbs only, and separately
save parsing errors.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import os
from collections import Counter


def get_indices(fpath):
    """
    Get position of target verbs in the context windows in a data file.
    :param fpath: path of data file
    :return: list of indices of target verbs
    """

    with open(fpath) as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [int(row[2]) for row in reader]

    return indices


def get_register(fpath):
    """
    Get register of data points in a data file.
    :param fpath: path of data file
    :return: list of registers for data points ('w' or 'r')
    """
    with open(fpath) as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [row[-1] for row in reader]

    return indices


def main():
    """
    Main method.
    """
    # Get individual verb parse files
    parse_dir = 'parses/'
    parse_files = os.listdir(parse_dir)
    parse_fnames = [f for f in parse_files if 'parses.txt' in f]
    parse_fnames.sort()

    verb_parses = []
    parse_errors = []

    for fname in parse_fnames:
        print(fname)
        parses = open(os.path.join(parse_dir, fname), 'r').read().split('\n')

        # Get indices of target verbs
        fnum = fname.split('_')[0]
        stem = fname.split('_')[1]
        indices = get_indices(f'../d2_data/joined/{fnum}_{stem}_joined.tsv')
        registers = get_register(f'../d2_data/joined/{fnum}_{stem}_joined.tsv')

        # Get target verbs and parses with errors
        for i in range(len(indices)):
            cur_parses = [p for p in parses[i][1:-1].split(', ')
                          if ':Punc' not in p]

            if 'UNK' not in cur_parses[indices[i]]:
                new_line = f'{cur_parses[indices[i]]} {registers[i]} {stem}'
                verb_parses.append(new_line)
            else:
                parse_errors.append(cur_parses[indices[i]])

    print(len(verb_parses), len(verb_parses)-len(parse_errors))
    print(len(parse_errors))

    # Save data and parse errors
    with open('verb_parses.txt', 'w') as f:
        f.write('\n'.join(verb_parses))

    parse_error_counter = Counter(parse_errors)
    parse_errors = sorted(list(set(parse_errors)),
                          key=lambda x: parse_error_counter[x], reverse=True)

    with open('parse_errors.txt', 'w') as f:
        lines = [f'{k} {parse_error_counter[k]}' for k in parse_errors]
        f.write('\n'.join(lines))
        f.wr


if __name__ == '__main__':
    main()
    exit(0)
