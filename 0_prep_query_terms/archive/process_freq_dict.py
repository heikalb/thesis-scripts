"""
Extract highest frequency verb stems from the text file of the Frequency Dictionary of Turkish.
Heikal Badrulhisham <heikal93gmail.com>, 2019
"""
import re


def main():
    # Section of the dictionary with the verb stems
    verb_section = open('freq_dict_.txt', 'r').read().split('\n')[54671:58256]
    # Isolate verb stems
    stems = [line.split()[0] for line in verb_section if len(line.split()) >= 3 and line.split()[1] == 'to']
    stems = [s for s in stems if s != 'to' and not any(c in s for c in ';,')]

    # Spell correction
    h_words = ['hazırla', 'hisset', 'hesapla', 'bahset', 'harca', 'hızlan', 'hedefle', 'rahatla', 'hohlan', 'hallet', 'zehirle',
               'haykır', 'heyecan', 'hükmet', 'hafifle', 'havalan', 'hastalan', 'hahla', 'fethet', 'sahiplen', 'hapset',
               'hareketlen', 'buharlah', 'hıçkır', 'hüphelen', 'mahvet', 'kamah', 'hırpala', 'hatırla']
    h_correction = {'hohlan': 'hoşlan', 'hahla': 'haşla', 'buharlah': 'buharlaş', 'hüphelen': 'şüphelen', 'kamah': 'kamaş'}
    stems_ = []

    for s in stems:
        s = s.replace('j', 'ğ')
        if s not in h_words:
            stems_.append(s.replace('h', 'ş'))
        elif s in h_correction:
            stems_.append(h_correction[s])
        else:
            stems_.append(s)

    # Save 1_data
    with open('freq_dict_verbs_.txt', 'w') as f:
        f.write('\n'.join(stems_))


if __name__ == '__main__':
    main()
    exit(0)
