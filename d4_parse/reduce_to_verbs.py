"""
Reduce the file of parses to parses of target verbs only.
"""
import csv
import os


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
            verb_parses.append('{0} {1}'.format(crnt_parses[indices[i]], registers[i]))

            if 'UNK' in crnt_parses[indices[i]]:
                parse_errors.append(crnt_parses[indices[i]])

    # Save data
    with open('verb_parses.txt', 'w') as f:
        f.write('\n'.join(verb_parses))

    with open('parse_errors.txt', 'w') as f:
        f.write('\n'.join(parse_errors))


if __name__ == '__main__':
    main()
    exit(0)
