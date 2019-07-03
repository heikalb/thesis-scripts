"""
Reduce the file of parses to parses of target verbs only.
"""
import csv
import os
from collections import Counter


# Get position of target verbs in the context windows
def get_verb_indices(fpath):
    with open(fpath) as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [int(row[2]) for row in reader]

    return indices


def get_register(fpath):
    with open(fpath) as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [row[-1] for row in reader]

    return indices


def main():
    # Get individual verb parse files
    parse_dir_path = 'parses/'
    parse_fnames = [fn for fn in os.listdir(parse_dir_path) if 'parses.txt' in fn]
    parse_fnames.sort()
    verb_parses = []
    parse_errors = []
     
    for fname in parse_fnames:
        print(fname)
        parses = open(os.path.join(parse_dir_path, fname), 'r').read().split('\n')

        # Get indices of target verbs
        fnum = fname.split('_')[0]
        stem = fname.split('_')[1]
        indices = get_verb_indices('../d2_data/joined/{0}_{1}_joined.tsv'.format(fnum, stem))
        registers = get_register('../d2_data/joined/{0}_{1}_joined.tsv'.format(fnum, stem))

        # Get target verbs and parses with errors
        for i in range(len(indices)):
            crnt_parses = [p for p in parses[i][1:-1].split(', ') if ':Punc' not in p]

            if 'UNK' not in crnt_parses[indices[i]]:
                verb_parses.append(f'{crnt_parses[indices[i]]} {registers[i]} {stem}')
            else:
                parse_errors.append(crnt_parses[indices[i]])

    print(len(verb_parses), len(verb_parses)-len(parse_errors))
    print(len(parse_errors))

    # Save data and parse errors
    with open('verb_parses.txt', 'w') as f:
        f.write('\n'.join(verb_parses))

    parse_error_counter = Counter(parse_errors)
    parse_errors = sorted(list(set(parse_errors)), key=lambda x: parse_error_counter[x], reverse=True)

    with open('parse_errors.txt', 'w') as f:
        # f.write('\n'.join(parse_errors))
        f.write('\n'.join([f'{k} {parse_error_counter[k]}' for k in parse_errors]))


if __name__ == '__main__':
    main()
    exit(0)
