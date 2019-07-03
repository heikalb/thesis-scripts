"""
Get various collocation statistics on stems and trigrams
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
from collections import defaultdict
from nltk import ngrams
import re
import sys
sys.path.append('../')
import colloc_measures as cm
import get_stats


# Count trigrams and stem-trigram pairs
def tally(pos, suff_boundary, morph_boundary, register=''):
    for parse in parses:
        # Decompose information on parse file line
        parse = parse.split()

        # Skip parses for a different stem or wrong parses
        if (pos not in parse[0] and pos not in parse[1]) or (register and register != parse[2]):
            continue

        # Get suffixes
        stem = parse[-1]
        suffixes = re.split(suff_boundary, parse[1])[1:]
        suffixes = get_stats.remove_forbidden_suffixes(suffixes)
        suffixes = [re.sub(morph_boundary, '', s) for s in suffixes]

        # Get trigrams
        curr_trigrams = ngrams(suffixes, 3)

        # Update frequency data
        frequency[stem] += 1

        for g in curr_trigrams:
            frequency[g] += 1
            pair_frequency[(stem, g)] += 1


# Get various association score for collocate pairs
def calc_assoc_score(total, measure_vals):
    for pair in pair_frequency:
        if pair[1] not in target_trigrams:
            continue

        stem, trigram = pair
        args = [frequency[stem], frequency[trigram], pair_frequency[pair], total, stem, trigram, pair_frequency]
        stat = cm.risk_ratio(*args)
        measure_vals[pair] = stat[0]


# Save data
def save_data(measure_vals):
    # Save stem-trigram association data
    with open('stem_trigram_rr.csv', 'w') as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow(['Stem', "Trigram", 'relative_risk'] +
                            ['stem_frequency', 'trigram_frequency', 'pair_frequency'])

        pairs = [k for k in pair_frequency if type(k) == tuple and len(k) == 2]
        pairs.sort(key=lambda x: measure_vals[x], reverse=True)

        for k in pairs:
            csv_writer.writerow([k[0], k[1], measure_vals[k]] + [frequency[s] for s in k] + [pair_frequency[k]])

    # Save trigrams
    with open('suffix_trigrams.txt', 'w') as f:
        f.write('\n'.join([f'{e} {frequency[e]}' for e in frequency if type(e) == tuple]))


def colloc_stats(pos, suff_boundary, morph_boundary):
    measure_vals = defaultdict(float)

    # Tally suffixes and suffix collocates
    tally(pos, suff_boundary, morph_boundary)

    # Get number of trigrams/stems
    total = sum(pair_frequency[p] for p in pair_frequency)

    # Get association measures
    calc_assoc_score(total, measure_vals)

    # Save stats in files
    save_data(measure_vals)


if __name__ == "__main__":
    # Open morphological parse file
    with open('../../d4_parse/verb_parses.txt', 'r') as f:
        parses = [p for p in f.read().split('\n')]

    # Frequency data
    frequency = defaultdict(int)
    pair_frequency = defaultdict(int)

    # Specific trigrams to get data on
    target_trigrams = [('PastPart→Noun', 'P3sg', 'Abl'), ('Pass→Verb', 'Inf2→Noun', 'P3pl'),
                       ('Neg', 'PastPart→Noun', 'A3pl'), ('Neg', 'PastPart→Noun', 'A3pl'),
                       ('FutPart→Noun', 'P3sg', 'Acc'), ('Inf2→Noun', 'P3sg', 'Acc'), ('Inf2→Noun', 'P3sg', 'Dat'),
                       ('Able→Verb', 'Neg', 'Aor'), ('PastPart→Noun', 'P3pl', 'Acc'), ('PastPart→Noun', 'P3sg', 'Dat')]

    # Get data
    colloc_stats('Verb', r'[\|\+]', r'.*:')
    exit(0)
