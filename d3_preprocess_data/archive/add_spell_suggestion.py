# -*- coding: utf-8 -*-
"""
Add manually identified spelling substitutions to the verb spelling correction suggestion file.
Heikal Badrulhisham, 2019
"""

import re
# Spelling substitutions
suggestions = {
    r'uo([mdl].+)?$':              'uyor',
    r'ıo([mdl].+)?$':              'ıyor',
    r'io([mdl].+)?$':              'iyor',
    r'üo([mdl].+)?$':              'üyor',
    r'iyo([mdl].+)?$':            'iyor',
    r'ıyo([mdl].+)?$':            'ıyor',
    r'uyo([mdl].+)?$':            'uyor',
    r'üyo([mdl].+)?$':            'üyor',

    r'iom$':            'iyorum',
    r'ıom$':            'ıyorum',
    r'iyom$':           'iyorum',
    r'ıyom$':           'ıyorum',
    r'uyom$':           'uyorum',
    r'üyom$':           'üyorum',

    r'iyon$':           'iyorsun',
    r'uyon$':           'uyorsun',
    r'ıyon$':           'ıyorsun',
    r'üyon$':           'üyorsun',

    r'iyoz$':           'iyoruz',
    r'ıyoz$':           'ıyoruz',
    r'uyoz$':           'uyoruz',
    r'üyoz$':           'üyoruz',

    r'ioz$':            'iyoruz',
    r'ıoz$':            'ıyoruz',
    r'iyoz$':           'iyoruz',
    r'ıyoz$':           'ıyoruz',
    r'uyoz$':           'uyoruz',
    r'üyoz$':           'üyoruz',

    r'micek':           'meyecek',
    r'mıcek':           'mayacak',
    r'[uı]cak':         'acak',
    r'icek':            'ecek',
    r'iycek':           'eyecek',
    r'ıycak':           'ayacak',

    r'[ıau]caz$':       'acağız',
    r'[ie]cez$':        'eceğiz',
    r'micez$':          'meyeceğiz',
    r'mıcaz$':          'mayacağız',
    r'iycez$':          'eyeceğiz',
    r'ıycaz$':          'ayacağız',

    r'[au]cam$':        'acağım',
    r'[ie]cem$':        'eceğim',
    r'mıcam$':          'mayacağım',
    r'micem$':          'meyeceğim',
    r'iycem':           'eyecem',
    r'ıycam':           'ayacam',

    r'e+cen$':          'eceksin',
    r'[au]+can$':       'acaksın',
    
    r'̇z':           'z',
    r'̇r':           'r',
    r'̇̇̇ṁ':           'm',
    r'̇̇̇ẏ':           'y'
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
    with open('verb_spelling_suggestions_.txt', 'w') as f:
        f.write('\n'.join(new_spelling))


if __name__ == '__main__':
    main()
    exit()
