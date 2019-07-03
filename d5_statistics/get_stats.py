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
def tally(stem, pos, suff_boundary, morph_boundary, suff_freq, pair_freq, adj_inst, bound=-1, register='', stem_frequency=None):
    for parse in parses:
        parse = parse.split()

        # Skip parses for a different stem or wrong parses
        stem_in_parse = parse[1].split(':')[0]
        if (stem and stem_in_parse not in stem) or (pos not in parse[0] and pos not in parse[1]) or (register and register != parse[2]):
            continue

        # Get suffixes, exclude stems. Collapse allomorphs. Remove unneeded suffixes the parser introduced
        suffixes = re.split(suff_boundary, parse[1])[1:]
        suffixes = remove_forbidden_suffixes(suffixes)
        suffixes = [re.sub(morph_boundary, '', s) for s in suffixes]

        # Get counts
        for i in range(len(suffixes)):
            # Single suffix frequency
            suff_freq[suffixes[i]] += 1

            # Regulate locality
            d = 0

            # Suffix pair cooccurrence frequency
            for j in range(i + 1, len(suffixes)):
                curr_pair = (suffixes[i], suffixes[j])
                pair_freq[curr_pair] += 1

                # Frequency of the two suffixes being adjacent
                if j - i == 1:
                    adj_inst[curr_pair] += 1

                # Keep count local
                d += 1
                if bound != -1 and d >= bound:
                    break

                # Count verb stem frequency of pairs
                if parse[3] not in stem_frequency[curr_pair]:
                    stem_frequency[curr_pair].append(parse[3])

    # Report frequencies
    print(f'Stem: {stem}\tPair types: {len(pair_freq)}\tPair instances: {sum([pair_freq[p] for p in pair_freq])}')


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
            args = [suff_freq[suff_1], suff_freq[suff_2], pair_freq[pair], num_suffixes, suff_1, suff_2, pair_freq]
            stat = measure_funct[msr](*args)

            if type(stat) == tuple:
                measure_vals[msr][pair] = stat[0]
                ci_dict[msr][pair] = stat[1]
            else:
                measure_vals[msr][pair] = stat


# Save data
def save_data(suff_freq, pair_freq, faffix, dir_affix, stem, measure_vals, ci_dict, adj_inst, stem_frequency):
    # Create file if it's not alreeady there
    if not os.path.isdir(f'association_stats{dir_affix}'):
        os.mkdir(f'association_stats{dir_affix}')

    # Fill up data
    with open(f'association_stats{dir_affix}/{faffix}_{stem}_association_stats{dir_affix}.csv', 'w') as f:
        csv_writer = csv.writer(f)

        # Column labels
        csv_writer.writerow(["collocate_pair"] + [m for m in measure_vals] +
                            ['{0}_confidence_interval_{1}'.format(k, d) for k in measure_confidence_interval for d in ['left', 'right']] +
                            ['suffix1_frequency', 'suffix2_frequency', 'suffix1-suffix2_frequency',
                             'suffix1-suffix2_adjacent_frequency', 'stem_frequency'])

        # Fill in row values, sort by risk ratio
        for k in sorted(pair_freq, key=lambda x: measure_vals['risk_ratio'][x], reverse=True):
            csv_writer.writerow([k] + [measure_vals[msr][k] for msr in measure_vals] +
                                [ci_dict[c][k][i] for c in ci_dict for i in [0, 1]] +
                                [suff_freq[suff] for suff in k] + [pair_freq[k], adj_inst[k], len(stem_frequency[k])])


def colloc_stats(pos, suff_boundary, morph_boundary, stem="", file_affix="", dir_affix='', register='', bound=-1):
    # Dictionaries for various frequency variables
    measure_vals = dict(zip(measures, [dict() for m in measures]))
    ci_dict = dict(zip(measure_confidence_interval, [dict() for m in measure_confidence_interval]))
    suff_freq, pair_freq = defaultdict(int), defaultdict(int)
    adj_inst = defaultdict(int)
    stem_frequency = defaultdict(list)

    # Tally suffixes and suffix collocates
    tally(stem, pos, suff_boundary, morph_boundary, suff_freq, pair_freq, adj_inst, bound, register, stem_frequency)

    # Get number of suffix instances (size of sample)
    num_suffixes = sum(suff_freq[s] for s in suff_freq)

    # Get association measures
    calc_assoc_score(suff_freq, pair_freq, num_suffixes, measure_vals, ci_dict)

    # Save stats in files
    save_data(suff_freq, pair_freq, file_affix, dir_affix, stem, measure_vals, ci_dict, adj_inst, stem_frequency)


if __name__ == "__main__":
    # Statistics
    measures = ['risk_ratio', 'risk_ratio_reverse', 'odds_ratio', 'mutual_information', 'dice_coefficient', 't_score',
                'chi_squared']
    measure_confidence_interval = ['risk_ratio', 'risk_ratio_reverse']
    measure_funct = dict(zip(measures, [cm.risk_ratio, cm.risk_ratio_reverse, cm.odds_ratio, cm.mutual_info,
                                        cm.dice_coeff, cm.t_score, cm.chi_sq]))

    # Get parses, stems, and file indices
    with open('../d4_parse/verb_parses.txt', 'r') as f:
        parses = [p for p in f.read().split('\n')]
    
    # File stems and indices. Empty string for selecting all verb stems
    stems = [""] + open('../d0_prep_query_terms/freq_dict_verbs.txt', 'r').read().split('\n')
    i = 0

    # Get statistics for each verb type
    for stem in stems:
        colloc_stats('Verb', r'[\|\+]', r'.*:', stem, f'00{i}'[-3:])
        # colloc_stats('Verb', r'[\|\+]', r'.*:', stem, f'00{str(i)}'[-3:], '_written', 'w')
        # colloc_stats('Verb', r'[\|\+]', r'.*:', stem, f'00{str(i)}'[-3:], '_spoken', 's')
        i += 1

    exit(0)
