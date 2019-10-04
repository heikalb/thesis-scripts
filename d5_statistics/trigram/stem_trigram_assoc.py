"""
Get association data on stems and trigrams
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import re
import sys
from nltk import ngrams
from collections import defaultdict
from collections import Counter
sys.path.append('../')
import colloc_measures as cm
import get_stats


def tally():
    """
    Get frequency of stems, trigrams and stem-trigram pairs
    """
    for parse in parses:
        # Decompose information on parse file line
        parse = parse.split()

        # Get suffixes
        stem = parse[-1]
        suffixes = re.split(suff_boundary, parse[1])[1:]
        suffixes = get_stats.remove_forbidden_suffixes(suffixes)
        suffixes = [re.sub(morph_boundary, '', s) for s in suffixes]

        curr_trigrams = ngrams(suffixes, 3)
        # curr_trigrams = tuple(suffixes)

        # Update frequency data
        frequency[stem] += 1

        for g in curr_trigrams:
            frequency[g] += 1
            pair_frequency[(stem, g)] += 1


def calc_association():
    """
    Calculate risk ratios of stem-trigram pairs
    """
    for pair in pair_frequency:
        # Only do for specified trigrams
        if pair[1] not in target_trigrams:
            continue

        # Get collocate members
        stem, trigram = pair

        # Get total number of stem-trigram pairs
        total = sum(pair_frequency[p] for p in pair_frequency)

        # Calculate risk ratio, even in reverse orientation
        args = [frequency[stem], frequency[trigram], pair_frequency[pair],
                total, stem, trigram, pair_frequency]

        risk_ratio[pair] = cm.risk_ratio(*args)[0]
        risk_ratio_reverse[pair] = cm.risk_ratio_reverse(*args)[0]


def save_data():
    """
    Save risk ratio data in a .csv file
    """
    # Save stem-trigram association data
    with open('stem_trigram_rr_.csv', 'w') as f:
        csv_writer = csv.writer(f)

        # Write file header
        header = ['stem', 'trigram', 'risk_ratio', 'risk_ratio_reverse',
                  'stem_frequency', 'trigram_frequency', 'pair_frequency']

        csv_writer.writerow(header)

        # Sort pairs by risk ratio
        pairs = [k for k in pair_frequency if type(k) == tuple and
                 len(k) == 2 and k[1] in target_trigrams]

        pairs.sort(key=lambda x: risk_ratio[x], reverse=True)

        # Write conntent data
        for k in pairs:
            row = [k[0], k[1], risk_ratio[k], risk_ratio_reverse[k],
                   *[frequency[s] for s in k], pair_frequency[k]]

            csv_writer.writerow(row)

    # Save trigrams
    with open('suffix_trigrams_.txt', 'w') as f:
        f.write('\n'.join([f'{e} {frequency[e]}'
                           for e in frequency if type(e) == tuple]))


if __name__ == "__main__":
    # Open morphological parse file
    with open('../../d4_parse/verb_parses.txt', 'r') as f:
        parses = [p for p in f.read().split('\n')]

    # For counting stem frequency of trigrams
    stems = [p.split()[-1] for p in parses]
    stems = Counter(stems)

    # Frequency data
    frequency = defaultdict(int)
    pair_frequency = defaultdict(int)

    # Specific trigrams to get data on
    target_trigrams = [('PastPart→Noun', 'P3sg', 'Acc'),
                       ('Pass→Verb', 'Inf2→Noun', 'P3sg'),
                       ('Neg', 'PastPart→Noun', 'P3sg'),
                       ('Pass→Verb', 'PastPart→Noun', 'P3sg'),
                       ('FutPart→Noun', 'P3sg', 'Acc'),
                       ('Inf2→Noun', 'P3sg', 'Acc'),
                       ('Inf2→Noun', 'P3sg', 'Dat'),
                       ('Able→Verb', 'Neg', 'Aor'),
                       ('PastPart→Noun', 'P3pl', 'Acc'),
                       ('PastPart→Noun', 'P3sg', 'Dat')]

    # For segmenting parses
    pos = 'Verb'
    suff_boundary = r'[\|\+]'
    morph_boundary = r'.*:'

    # Store risk ratio values
    risk_ratio = dict()
    risk_ratio_reverse = dict()

    # Tally trigrams and stem-trigram collocates
    tally()

    # Get risk ratio
    calc_association()

    # Save data in files
    save_data()
    exit(0)
