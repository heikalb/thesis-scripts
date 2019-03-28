"""
Extract highest frequency verb stems from the text file of the Frequency Dictionary of Turkish.
Heikal Badrulhisham <heikal93gmail.com>, 2019
"""
import re


def main():
    # Section of the dictionary with the verb stems
    verb_section = open('freq_dict.txt', 'r').read().split('\n')[75067:77349]
    verb_section = '\n'.join([line for line in verb_section if line])
    # Isolate verb stems
    verb_section = re.findall(r'\d+\s*\|\s*\d+\n*.+\sto.*', verb_section)
    verb_section = [line.replace('\n', ' ') for line in verb_section if line.split()[4] == 'to']
    stems = []

    # Get index number from dictionary for sorting the stems
    for line in verb_section:
        index = int(line.split('|')[0].strip())
        stem_line = ' '.join(line.split()[3:])
        stems.append((index, stem_line))

    # Account for error in txt file of the dictionary
    stems.append((699, 'yapılaş to strcuture'))
    stems.sort()

    # Spelling and morphological correction
    h_words = ['hazırla', 'hisset', 'hesapla', 'bahset', 'harca', 'hızlan', 'hedefle', 'rahatla', 'hohlan', 'hallet',
               'zehirle', 'haykır', 'heyecan', 'hükmet', 'hafifle', 'havalan', 'hastalan', 'hahla', 'fethet', 'sahiplen'
               , 'hapset', 'hareketlen', 'buharlah', 'hıçkır', 'hüphelen', 'mahvet', 'kamah', 'hırpala', 'hatırla'
               , 'haberleh', 'heyecanlan']
    h_correction = {'hohlan': 'hoşlan', 'hahla': 'haşla', 'buharlah': 'buharlaş', 'hüphelen': 'şüphelen',
                    'kamah': 'kamaş', 'haberleh': 'haberleş'}
    morph_correction = {'adlandır': 'adlan', 'bulundur': 'bulun', 'sınıflandır': 'sınıflan', 'görevlendir': 'görevlen',
                        'haberleş': 'haberle', 'abart': 'abar', 'kararlaştır': 'kararla', 'sınırlandır': 'sınırlan',
                        'ödüllendir': 'ödüllen', 'savrul': 'savrul', 'biçimlendir': 'biçimlen',
                        'ilişkilendir': 'ilişkilen', 'isimlendir': 'isimlen', 'anlamlandır': 'anlamlan',
                        'yardımlaş': 'yardımla'}

    stems_ = []

    for s in stems:
        s = s[1].split()[0]
        s = s.replace('j', 'ğ')
        if s not in h_words:
            s = s.replace('h', 'ş')
        elif s in h_correction:
            s = h_correction[s]

        if s in morph_correction:
            s = morph_correction[s]

        stems_.append(s)

    # Save data
    with open('freq_dict_verbs.txt', 'w') as f:
        f.write('\n'.join(stems_))


if __name__ == '__main__':
    main()
    exit(0)
