import csv
import os
import re
from collections import defaultdict


# Get position of target verbs in the context windows
def get_verb_indices(fpath):
    with open(fpath) as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [int(row[2]) for row in reader]

    return indices


def main():
    with open('../d4_parse/verbs_parses.txt', 'r') as f:
        parses = [p.split() for p in f.read().split('\n')]

    morphs = []
    morphemes = defaultdict(list)
    # Go through parses
    for parse in parses:
        # Get suffixes, exclude stems. Collapse allomorphs
        cur_parse = re.split(r'[\|\+]', parse[1])[1:]

        for cp in cur_parse:
            if len(cp.split(':')) == 2:
                morph = cp.split(':')[0]
                morpheme = cp.split(':')[1]
            else:
                morph = cp[0]
                morpheme = ""

            if morph not in morphemes[morpheme]:
                morphemes[morpheme].append(morph)

    for k in morphemes:
        print(k)
        print(morphemes[k])
        print('\n')

    # Save data
    with open('morphs.txt', 'w') as f:
        f.write('\n'.join(morphemes))


if __name__ == '__main__':
    main()
    exit(0)
