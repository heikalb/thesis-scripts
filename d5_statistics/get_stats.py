"""
Get various collocation d5_statistics from the corpus
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
from collections import defaultdict
import re
import colloc_measures as cm
import os

# Statistics
measures = ['mutual_information', 't_score', 'dice_coefficient', 'chi_squared', 'relative_risk', 'odds_ratio']
measure_funct = dict(zip(measures, [cm.mutual_info, cm.t_score, cm.dice_coeff, cm.chi_squared, cm.rel_risk,
                                    cm.odds_ratio]))


def new_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)


def colloc_stats(right_parse_sign, suffix_boundary, mboundary, query_term="", faffix=""):
    measure_dict = dict(zip(measures, [dict() for m in measures]))
    abs_msr = {'suff_freq': defaultdict(int), 'cooc_freq': defaultdict(int)}

    # Go through parses
    for parse in parses:
        # Skip parses for a different stem or wrong parses
        if query_term not in parse[0] or right_parse_sign not in parse[0]:
            continue

        # Get suffixes, exclude stems. Collapse allomorphs
        suffixes = re.split(suffix_boundary, parse[1])[1:]
        suffixes = [re.sub(mboundary, '', s) for s in suffixes]

        # Count suffix (co)occurrences
        for i in range(len(suffixes)):
            abs_msr['suff_freq'][suffixes[i]] += 1

            for j in range(i + 1, len(suffixes)):
                curr_pair = (suffixes[i], suffixes[j])
                abs_msr['cooc_freq'][curr_pair] += 1

    num_suffixes = sum(abs_msr['suff_freq'][s] for s in abs_msr['suff_freq'])

    # Get association measures
    for k in abs_msr['cooc_freq']:
        m1, m2 = k

        for msr in measures:
            args = [abs_msr['suff_freq'][m1], abs_msr['suff_freq'][m2], abs_msr['cooc_freq'][k], num_suffixes,
                    m1, m2, abs_msr['cooc_freq']]
            stat = measure_funct[msr](*args)

            if type(stat) == tuple:
                measure_dict[msr][k] = (stat[0], stat[1][0], stat[1][1], abs_msr['suff_freq'][m1], abs_msr['suff_freq'][m2])
            else:
                measure_dict[msr][k] = (stat, abs_msr['suff_freq'][m1], abs_msr['suff_freq'][m2])

    # Save data
    for msr in abs_msr:
        new_dir(msr)
        with open('{0}/{1}_{2}_{0}.csv'.format(msr, faffix, query_term), 'w') as f:
            csv_writer = csv.writer(f)

            for k in abs_msr[msr]:
                csv_writer.writerow([k, abs_msr[msr][k]])

    for msr in measures:
        new_dir(msr)
        with open('{0}/{1}_{2}_{0}.csv'.format(msr, faffix, query_term), 'w') as f:
            csv_writer = csv.writer(f)

            for k in measure_dict[msr]:
                csv_writer.writerow([k] + [datum for datum in measure_dict[msr][k]])


if __name__ == "__main__":
    # Open file of parses
    with open('../d4_parse/verbs_parses.txt', 'r') as f:
        parses = [p.split() for p in f.read().split('\n')]

    query_terms = [""] + open('../d0_prep_query_terms/freq_dict_verbs.txt', 'r').read().split('\n')
    query_terms.remove('savrul')
    # File indexes
    f_i = [""] + [('00'+str(i))[-3:] for i in range(len(query_terms))]

    i = 0
    for qt in query_terms:
        print(qt)
        colloc_stats(right_parse_sign='Verb', suffix_boundary=r'[\|\+]', mboundary=r'.*:', query_term=qt, faffix=f_i[i])
        i += 1

    exit(0)
