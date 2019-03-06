# -*- coding: utf-8 -*-
"""
Add manually identified spelling substitutions to the verb spelling correction suggestion file.
Heikal Badrulhisham, 2019
"""

import re
# Spelling substitutions
suggestions = {
    r'iom$':            'iyorum',
    r'ıom$':            'iyorum',
    r'uo':              'uyor',
    r'ıo':              'ıyor',
    r'io':              'iyor',
    r'iyo$':            'iyor',
    r'[uü]yo$':         'uyor',
    r'iyom$':           'iyorum',
    r'uyom$':           'uyorum',
    r'iyon$':           'iyorsun',
    r'uyon$':           'uyorsun',
    r'iyoz$':           'iyoruz',
    r'ıyoz$':           'ıyoruz',
    r'uyoz$':           'uyoruz',
    r'micek':           'meyecek',
    r'micez':           'meyeceğiz',
    r'[uı]cak':         'acak',
    r'icek':            'ecek',
    r'iycek':           'eyecek',
    r'ıycak':           'ayacak',
    r'[ıau]caz$':       'acağız',
    r'[ie]cez$':        'eceğiz',
    r'[au]cam$':        'acağım',
    r'[ie]cem$':        'eceğim',
    r'mıcam':           'mayacağım',
    r'micem':           'meyeceğim',
    r'e+cen$':          'eceksin',
    r'[au]+can$':       'acaksın',
    r'mıycak':          'mayacak',
    r'miycek':          'meyecek',
}


def main():
    # Current spellcheck file
    pres_spelling = open('verb_spellcheck.txt', 'r').read().split('\n')
    new_spelling = []

    # Go through file lines
    for line in pres_spelling:
        # Get the error word
        target = line.split()[0]
        # Default line to save
        new_line = line

        # Create a new line with a new correction candidate if there's a match
        for sug in suggestions:
            if re.search(sug, target):
                new_suggestion = re.sub(sug, suggestions[sug], target)
                new_line = ' '.join([target, new_suggestion, ' '.join(line.split()[1:])])
                break

        new_spelling.append(new_line)

    # Save modifications onto a new file
    with open('verb_spelling_suggestions_2_.txt', 'w') as f:
        f.write('\n'.join(new_spelling))


if __name__ == '__main__':
    main()
    exit()
