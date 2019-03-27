"""
Get various collocation 5_statistics from the corpus
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
from collections import defaultdict
import re
import colloc_measures as cm
import os


def new_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)


def colloc_stats(right_parse_sign, suffix_boundary, mboundary, key_separator, query_term=""):
    # Statistics
    measures = ['mutual_information', 't_score', 'dice_coefficient', 'chi_squared', 'relative_risk', 'odds_ratio']
    measure_funct = dict(zip(measures, [cm.mutual_info, cm.t_score, cm.dice_coeff, cm.chi_squared, cm.rel_risk,
                                        cm.odds_ratio]))
    measure_dict = dict(zip(measures, [dict() for m in measures]))
    abs_msr = {'suff_freq': defaultdict(int), 'cooc_freq': defaultdict(int)}

    # Open file of parses
    parses = open('../3_parse/parses_verbs.txt', 'r').read().split('\n')
    parses = [p.split() for p in parses]

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
                # curr_key = '{0}{1}{2}'.format(suffixes[i], key_separator, suffixes[j])
                curr_pair = (suffixes[i], suffixes[j])
                abs_msr['cooc_freq'][curr_pair] += 1

    num_suffixes = sum(abs_msr['suff_freq'][s] for s in abs_msr['suff_freq'])

    # Get association measures
    for k in abs_msr['cooc_freq']:
        m1, m2 = k

        for msr in measures:
            args = [abs_msr['suff_freq'][m1], abs_msr['suff_freq'][m2], abs_msr['cooc_freq'][k], num_suffixes,
                    m1, m2, abs_msr['cooc_freq']]
            measure_dict[msr][k] = (measure_funct[msr](*args), abs_msr['suff_freq'][m1], abs_msr['suff_freq'][m2])

    # Save data
    for m in abs_msr:
        new_dir(m)
        with open('{0}/{0}_{1}.csv'.format(m, query_term), 'w') as f:
            csv_writer = csv.writer(f)

            for k in abs_msr[m]:
                csv_writer.writerow([k, abs_msr[m][k]])

    for msr in measures:
        new_dir(msr)
        with open('{0}/{0}_{1}.csv'.format(msr, query_term), 'w') as f:
            csv_writer = csv.writer(f)

            for k in measure_dict[msr]:
                csv_writer.writerow([k, measure_dict[msr][k][0], measure_dict[msr][k][1], measure_dict[msr][k][2]])


def main():
    query_terms = [""] + open('../2_data/query_terms.txt', 'r').read().split('\n')

    for qt in query_terms:
        colloc_stats(right_parse_sign='Verb', suffix_boundary=r'[\|\+]', mboundary=r'.*:',
                     key_separator='__', query_term=qt)


if __name__ == "__main__":
    main()
    exit(0)
