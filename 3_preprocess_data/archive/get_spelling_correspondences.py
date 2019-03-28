import difflib

spellings = open('verb_spelling_suggestions_2.txt', 'r').read().split('\n')
changes = []

for sp in spellings:
    if '#' in sp or '@' in sp or not sp:
        continue

    error, correction = sp.split()[0:2]
    seqmatch = difflib.SequenceMatcher(None, error, correction)
    p1, p2, lgth = seqmatch.find_longest_match(0, len(error), 0, len(correction))
    common_string = error[p1: p2+lgth]

    error_sub = error[len(common_string):]
    correction_sub = correction[len(common_string):]

    if len(error_sub) < 3:
        error_sub = error[len(common_string)-2:]
        correction_sub = correction[len(common_string)-2:]

    if not error_sub == correction_sub:
        changes.append((error_sub, correction_sub))

changes = list(set(changes))
changes = ["r'{0}$': '{1}'".format(ch[0], ch[1]) for ch in changes]
changes.sort()
with open('spelling_correspondences.txt', 'w') as f:
    f.write(',\n'.join(changes))
