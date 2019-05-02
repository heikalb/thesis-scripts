"""
Get various collocation statistics from the corpus
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
from collections import defaultdict
import re
import colloc_measures as cm
import os

# Statistics
measures = ['relative_risk', 'odds_ratio', 'mutual_information', 't_score', 'dice_coefficient', 'chi_squared']
measures_w_ci = ['relative_risk']
measure_funct = dict(zip(measures, [cm.rel_risk, cm.odds_ratio, cm.mutual_info, cm.t_score, cm.dice_coeff, cm.chi_sq]))


# Count suffixes and collocate pairs
def tally(stem, pos, suff_boundary, morph_boundary, suff_freq, pair_freq, adj_inst, bound=-1, register=''):
    for parse in parses:
        # Skip parses for a different stem or wrong parses
        if stem not in parse[0] or pos not in parse[0] or (register and register != parse[2]):
            continue

        # Get suffixes, exclude stems. Collapse allomorphs. Remove unneeded suffixes the parser introduced
        suffixes = re.split(suff_boundary, parse[1])[1:]
        suffixes = remove_forbidden_suffixes(suffixes)
        suffixes = [re.sub(morph_boundary, '', s) for s in suffixes]

        # Count suffix (co)occurrences
        for i in range(len(suffixes)):
            suff_freq[suffixes[i]] += 1
            d = 0

            for j in range(i + 1, len(suffixes)):
                curr_pair = (suffixes[i], suffixes[j])
                pair_freq[curr_pair] += 1

                if j - i == 1:
                    adj_inst[curr_pair] += 1

                d += 1

                if bound != -1 and d >= bound:
                    break

    print(sum([pair_freq[k] for k in pair_freq]), 'pairs')


# Remove unneeded suffixes
def remove_forbidden_suffixes(suffixes):
    if suffixes[-1] == 'A3sg':
        return [suff for suff in suffixes if ':' in suff] + [suffixes[-1]]
    else:
        return [suff for suff in suffixes if ':' in suff]


# Get various association score for collocate pairs
def calc_assoc_score(suff_freq, pair_freq, num_suffixes, measure_dict, ci_dict):
    for k in pair_freq:
        m1, m2 = k

        for msr in measures:
            args = [suff_freq[m1], suff_freq[m2], pair_freq[k], num_suffixes, m1, m2, pair_freq]
            stat = measure_funct[msr](*args)

            if type(stat) == tuple:
                measure_dict[msr][k] = stat[0]
                ci_dict[msr][k] = stat[1]
            else:
                measure_dict[msr][k] = stat


# Save data
def save_data(suff_freq, pair_freq, faffix, dir_affix, stem, measure_dict, ci_dict, adj_inst):
    pairs = [p for p in pair_freq]

    if not os.path.isdir('assoc_stats{0}'.format(dir_affix)):
        os.mkdir('assoc_stats{0}'.format(dir_affix))

    with open('assoc_stats{0}/{1}_{2}_assoc_stats{3}.csv'.format(dir_affix, faffix, stem, dir_affix), 'w') as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow(["collocate_pair"] + [m for m in measures] +
                            ['{0}_ci_{1}'.format(k, d) for k in measures_w_ci for d in ['left', 'right']] +
                            ['s1_frequency', 's2_frequency', 's1s2_frequency', 's1s2_adjacent_frequency'])

        for k in sorted(pair_freq, key=lambda x: measure_dict['relative_risk'][x], reverse=True):
            if suff_freq[k[0]] >= 100 and suff_freq[k[1]] >= 100:
                csv_writer.writerow([k] + [measure_dict[msr][k] for msr in measure_dict] +
                                    [ci_dict[c][k][i] for c in ci_dict for i in [0, 1]] +
                                    [suff_freq[suff] for suff in k] + [pair_freq[k], adj_inst[k]])


def colloc_stats(pos, suff_boundary, morph_boundary, stem="", faffix="", dir_affix='', register='', bound=-1):
    measure_dict = dict(zip(measures, [dict() for m in measures]))
    ci_dict = dict(zip(measures_w_ci, [dict() for m in measures_w_ci]))
    suff_freq, pair_freq = defaultdict(int), defaultdict(int)
    adj_inst = defaultdict(int)

    # Tally suffixes and suffix collocates
    tally(stem, pos, suff_boundary, morph_boundary, suff_freq, pair_freq, adj_inst, bound, register)

    # Get number of suffix instances (size of sample)
    num_suffixes = sum(suff_freq[s] for s in suff_freq)

    # Get association measures
    calc_assoc_score(suff_freq, pair_freq, num_suffixes, measure_dict, ci_dict)

    # Save stats in files
    save_data(suff_freq, pair_freq, faffix, dir_affix, stem, measure_dict, ci_dict, adj_inst)


if __name__ == "__main__":
    # Get parses, stems, and file indices
    with open('../d4_parse/verb_parses.txt', 'r') as f:
        parses = [p.split() for p in f.read().split('\n')]

    stems = [""] + open('../d0_prep_query_terms/freq_dict_verbs.txt', 'r').read().split('\n')
    stems.remove('savrul')
    f_i = [""] + [('00'+str(i))[-3:] for i in range(len(stems))]

    # Get statistics for each verb type
    for stem in stems:
        print(stem)
        # colloc_stats('Verb', r'[\|\+]', r'.*:', stem, f_i[stems.index(stem)])
        # colloc_stats('Verb', r'[\|\+]', r'.*:', stem, f_i[stems.index(stem)], '_written', 'w')
        colloc_stats('Verb', r'[\|\+]', r'.*:', stem, f_i[stems.index(stem)], '_spoken', 's')

    exit(0)
