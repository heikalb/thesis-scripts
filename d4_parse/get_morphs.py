"""
Get the morphs of morphemes
Heikal Badrulhisam <heikal93@gmail.com>, 2019
"""
import re
from collections import defaultdict


def main():
    """
    Main method.
    """
    # Open parse file
    with open('verb_parses.txt', 'r') as f:
        parses = [p.split() for p in f.read().split('\n')]

    # Map morphemes to lists of allomorphs
    morphemes = defaultdict(list)

    # Go morphs attached to verbs
    for parse in parses:
        # Get suffixes, exclude stems
        suffixes = re.split(r'[|+]', parse[1])[1:]

        for suffix in suffixes:
            if len(suffix.split(':')) == 2:
                exponent = suffix.split(':')[0]
                morpheme = suffix.split(':')[1]
            else:
                exponent = suffix[0]
                morpheme = ""

            if exponent not in morphemes[morpheme]:
                morphemes[morpheme].append(exponent)

    # Save data
    with open('morphs.txt', 'w') as f:
        f.write('\n'.join(k + ": " + str(morphemes[k]) for k in morphemes))


if __name__ == '__main__':
    main()
    exit(0)
