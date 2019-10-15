"""
Extract highest frequency verb stems from the Frequency Dictionary of Turkish.
Heikal Badrulhisham <heikal93gmail.com>, 2019
"""
import re


def get_indices_stems(freq_dict):
    """
    Get pairs of frequency indices and verb stems from the Frequency Dictionary
    :param freq_dict: .txt file of the Frequency Dictioary
    :return: list of index-verb stem pairs
    """

    # Section of the dictionary with the verb stems
    verb_section = freq_dict.read().split('\n')[75067:77349]
    verb_section = '\n'.join([line for line in verb_section if line])

    # Isolate verb stems
    verb_lines = re.findall(r'\d+\s*\|\s*\d+\n*.+\sto.*', verb_section)

    verb_lines = [line.replace('\n', ' ') for line in verb_lines
                  if line.split()[4] == 'to']

    # Pairs of frequency indices and stems
    indices_stems = []

    # Get frequency indices from the dictionary for sorting the stems
    for line in verb_lines:
        index = int(line.split('|')[0].strip())
        stem_line = ' '.join(line.split()[3:])
        indices_stems.append((index, stem_line))

    return indices_stems


def stem_correction(stem_index, h_words, h_corrections, morph_corrections):
    """
    Apply spelling and morphological corrections to stems

    :param stem_index: pair of verb stem and its index
    :param h_words: list of misspelled words involving 'ş'
    :param h_corrections: list of correct spelling for words involving 'ş'
    :param morph_corrections: list of morphological mappings
    :return: corrected stem
    """
    stem = stem_index[1].split()[0]
    stem = stem.replace('j', 'ğ')

    if stem not in h_words:
        stem = stem.replace('h', 'ş')
    elif stem in h_corrections:
        stem = h_corrections[stem]

    if stem in morph_corrections:
        stem = morph_corrections[stem]

    return stem


def main():
    """
    Extract verbs from the Frequency Dictionary and save them in a .txt file.
    """

    # Open Frequency Disctionary file
    freq_dict = open('freq_dict.txt', 'r')

    # Get pairs of frequency indices and verb stems
    indices_stems = get_indices_stems(freq_dict)

    # Account for error in txt file of the dictionary
    indices_stems.append((699, 'yapılaş to strcuture'))

    # For spelling and morphological correction
    h_words = ['hazırla', 'hisset', 'hesapla', 'bahset', 'harca',
               'hızlan', 'hedefle', 'rahatla', 'hohlan', 'hallet',
               'zehirle', 'haykır', 'heyecan', 'hükmet', 'hafifle',
               'havalan', 'hastalan', 'hahla', 'fethet', 'sahiplen',
               'hapset', 'hareketlen', 'buharlah', 'hıçkır', 'hüphelen',
               'mahvet', 'kamah', 'hırpala', 'hatırla', 'haberleh',
               'heyecanlan']

    h_corrections = {'hohlan': 'hoşlan', 'hahla': 'haşla',
                     'buharlah': 'buharlaş', 'hüphelen': 'şüphelen',
                     'kamah': 'kamaş', 'haberleh': 'haberleş'}

    morph_corrections = {'adlandır': 'adlan', 'bulundur': 'bulun',
                         'sınıflandır': 'sınıflan', 'görevlendir': 'görevlen',
                         'haberleş': 'haberle', 'abart': 'abar',
                         'kararlaştır': 'kararla', 'sınırlandır': 'sınırlan',
                         'ödüllendir': 'ödüllen', 'savrul': 'savrul',
                         'biçimlendir': 'biçimlen', 'ilişkilendir': 'ilişkilen',
                         'isimlendir': 'isimlen', 'anlamlandır': 'anlamlan',
                         'yardımlaş': 'yardımla'}

    # For storing corrected verb stems
    corrected_stems = []

    # Apply corrections to verb stems
    for index_stem in sorted(indices_stems):
        corrected_stem = stem_correction(index_stem, h_words, h_corrections,
                                         morph_corrections)

        corrected_stems.append(corrected_stem)

    # Save data
    with open('freq_dict_verbs.txt', 'w') as f:
        f.write('\n'.join(corrected_stems))


if __name__ == '__main__':
    main()
    exit(0)
