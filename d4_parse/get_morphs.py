"""
Get the morphs of morphemes
Heikal Badrulhisam <heikal93@gmail.com>, 2019
"""
import re
from collections import defaultdict


def main():
    """
    Get the morphs of morphemes in a file of morphological parses and save the
    morphs found in a .txt file.
    """
    # Open parse file
    with open('verb_parses.txt', 'r') as f:
        parses = [p.split() for p in f.read().split('\n')]

    # Map morphemes to lists of allomorphs
    morphemes = defaultdict(list)

    # Go morphs attached to verbs
    for parse in parses:
        # Get suffixes, exclude stems
        cur_parse = re.split(r'[|+]', parse[1])[1:]

        for cp in cur_parse:
            if len(cp.split(':')) == 2:
                morph = cp.split(':')[0]
                morpheme = cp.split(':')[1]
            else:
                morph = cp[0]
                morpheme = ""

            if morph not in morphemes[morpheme]:
                morphemes[morpheme].append(morph)

    # Save data
    with open('morphs.txt', 'w') as f:
        f.write('\n'.join(k + ": " + str(morphemes[k]) for k in morphemes))


if __name__ == '__main__':
    main()
    exit(0)
