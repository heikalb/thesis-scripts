"""
Get various collocation statistics from the corpus
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
from collections import defaultdict
import re
import colloc_measures as cm
import os


# Count suffixes and collocate pairs
def tally(stem, suff_freq, pair_freq, adj_inst, stem_frequency, register=''):

    for parse in parses:
        parse = parse.split()

        # Skip parses for a different stem or wrong parses
        stem_in_parse = parse[1].split(':')[0]

        if (stem and stem_in_parse not in stem) or \
           (pos not in parse[0] and pos not in parse[1]) or \
           (register and register != parse[2]):
            continue

        # Get suffixes, exclude stems. Collapse allomorphs.
        # Remove unneeded suffixes the parser introduced
        suffixes = re.split(suffix_boundary, parse[1])[1:]
        suffixes = remove_forbidden_suffixes(suffixes)
        suffixes = [re.sub(morph_boundary, '', s) for s in suffixes]

        # Get counts
        for i in range(len(suffixes)):
            # Single suffix frequency
            suff_freq[suffixes[i]] += 1

            # Suffix pair cooccurrence frequency
            for j in range(i + 1, len(suffixes)):
                curr_pair = (suffixes[i], suffixes[j])
                pair_freq[curr_pair] += 1

                # Frequency of the two suffixes being adjacent
                if j - i == 1:
                    adj_inst[curr_pair] += 1

                # Count verb stem frequency of pairs
                if parse[3] not in stem_frequency[curr_pair]:
                    stem_frequency[curr_pair].append(parse[3])

    print(sum([suff_freq[s] for s in suff_freq]))
    print(len([s for s in suff_freq]))

    print(sum([pair_freq[p] for p in pair_freq]))
    print(len([p for p in pair_freq]))

    print(len(stems))
    print(len(parses))

    exit()

    # Report frequencies
    print(f'Stem: {stem}\tPair types: {len(pair_freq)}\t'
          f'Pair instances: {sum([pair_freq[p] for p in pair_freq])}')


# Remove unneeded suffixes
def remove_forbidden_suffixes(suffixes):
    if suffixes[-1] == 'A3sg':
        return [suff for suff in suffixes if ':' in suff] + [suffixes[-1]]
    else:
        return [suff for suff in suffixes if ':' in suff]


# Get various association score for collocate pairs
def calc_assoc_score(suff_freq, pair_freq, num_suffixes, measure_vals, ci_dict):
    for pair in pair_freq:
        suff_1, suff_2 = pair

        for msr in measures:
            args = [suff_freq[suff_1], suff_freq[suff_2], pair_freq[pair],
                    num_suffixes, suff_1, suff_2, pair_freq]

            stat = measures[msr](*args)

            if type(stat) == tuple:
                measure_vals[msr][pair] = stat[0]
                ci_dict[msr][pair] = stat[1]
            else:
                measure_vals[msr][pair] = stat


# Save data
def save_data(suff_freq, pair_freq, faffix, dir_affix, stem, measure_vals,
              ci_dict, adj_inst, stem_frequency):

    # Create file if it's not alreeady there
    if not os.path.isdir(f'association_stats{dir_affix}'):
        os.mkdir(f'association_stats{dir_affix}')

    # Fill up data
    file_path = f'association_stats{dir_affix}/{faffix}_{stem}' +\
                f'_association_stats{dir_affix}.csv'

    with open(file_path, 'w') as f:
        csv_writer = csv.writer(f)

        # Column labels
        first_row = ["collocate_pair", *[m for m in measure_vals],
                     *[f'{k}_confidence_interval_{d}'
                       for k in confidence_intervals
                       for d in ['left', 'right']],
                     'suffix1_frequency', 'suffix2_frequency',
                     'suffix1-suffix2_frequency',
                     'suffix1-suffix2_adjacent_frequency', 'stem_frequency']

        csv_writer.writerow(first_row)

        # Fill in row values, sort by risk ratio
        sorted_pairs = sorted(pair_freq,
                              key=lambda x: measure_vals['risk_ratio'][x],
                              reverse=True)

        for k in sorted_pairs:
            row = [k, *[measure_vals[m][k] for m in measure_vals],
                   *[ci_dict[c][k][i] for c in ci_dict for i in [0, 1]],
                   *[suff_freq[suff] for suff in k],
                   pair_freq[k], adj_inst[k], len(stem_frequency[k])]

            csv_writer.writerow(row)


def colloc_stats(stem="", file_affix="", dir_affix='', register=''):
    # Dictionaries for various frequency variables
    measure_vals = dict(zip(measures, [dict() for m in measures]))

    ci_dict = dict(zip(confidence_intervals,
                       [dict() for m in confidence_intervals]))

    suff_freq, pair_freq = defaultdict(int), defaultdict(int)
    adj_inst = defaultdict(int)
    stem_frequency = defaultdict(list)

    # Tally suffixes and suffix collocates
    tally(stem, suff_freq, pair_freq, adj_inst, stem_frequency, register)

    # Get number of suffix instances (size of sample)
    num_suffixes = sum(suff_freq[s] for s in suff_freq)

    # Get association measures
    calc_assoc_score(suff_freq, pair_freq, num_suffixes, measure_vals, ci_dict)

    # Save stats in files
    save_data(suff_freq, pair_freq, file_affix, dir_affix, stem, measure_vals,
              ci_dict, adj_inst, stem_frequency)


if __name__ == "__main__":
    # Association measurements and confidence intervals
    measures = {'risk_ratio': cm.risk_ratio,
                'risk_ratio_reverse':  cm.risk_ratio_reverse,
                'odds_ratio': cm.odds_ratio,
                'mutual_information': cm.mutual_info,
                'dice_coefficient': cm.dice_coeff,
                't_score': cm.t_score,
                'chi_squared': cm.chi_sq}

    confidence_intervals = ['risk_ratio', 'risk_ratio_reverse']

    pos = 'Verb'
    suffix_boundary = r'[\|\+]'
    morph_boundary = r'.*:'

    # Get parses, stems, and file indices
    with open('../d4_parse/verb_parses.txt', 'r') as f:
        parses = [p for p in f.read().split('\n')]
    
    # File stems and indices. Empty string for selecting all verb stems
    verb_stems = open('../d0_prep_query_terms/freq_dict_verbs.txt', 'r')
    stems = [""] + verb_stems.read().split('\n')
    i = 0

    # Get statistics for each verb type
    for stem in stems:
        colloc_stats(stem, f'00{i}'[-3:])
        # colloc_stats(stem, f'00{i}'[-3:], dir_affix='_written', register='w')
        # colloc_stats(stem, f'00{i}'[-3:], dir_affix='_spoken', register='s')

        i += 1

    exit(0)
