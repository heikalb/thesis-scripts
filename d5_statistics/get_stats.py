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
measure_funct = dict(zip(measures, [cm.rel_risk, cm.odds_ratio, cm.mutual_info, cm.t_score, cm.dice_coeff, cm.chi_squared]))


def tally(query_term, right_parse_sign, suffix_boundary, mboundary, abs_msr, bound=-1):
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

            d = 0
            for j in range(i + 1, len(suffixes)):
                curr_pair = (suffixes[i], suffixes[j])
                abs_msr['cooc_freq'][curr_pair] += 1
                d += 1

                if bound != -1 and d >= bound:
                    break


def calc_assoc_score(abs_msr, num_suffixes, measure_dict, ci_dict):
    for k in abs_msr['cooc_freq']:
        if not k:
            continue

        m1, m2 = k

        for msr in measures:
            args = [abs_msr['suff_freq'][m1], abs_msr['suff_freq'][m2], abs_msr['cooc_freq'][k], num_suffixes,
                    m1, m2, abs_msr['cooc_freq']]
            stat = measure_funct[msr](*args)

            if type(stat) == tuple:
                measure_dict[msr][k] = stat[0]
                ci_dict[msr][k] = stat[1]
            else:
                measure_dict[msr][k] = stat


def save_data(abs_msr, faffix, query_term, measure_dict, ci_dict):
    # Save absolute frequency data
    for msr in abs_msr:
        if not os.path.isdir(msr):
            os.mkdir(msr)

        with open('{0}/{1}_{2}_{0}.csv'.format(msr, faffix, query_term), 'w') as f:
            csv_writer = csv.writer(f)

            for k in abs_msr[msr]:
                csv_writer.writerow([k, abs_msr[msr][k]])

    # Save association measures data
    if not os.path.isdir('assoc_stats'):
        os.mkdir('assoc_stats')

    with open('assoc_stats/{0}_{1}_assoc_stats.csv'.format(faffix, query_term), 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["collocate_pair"] +
                            [m for m in measures] +
                            ['{0}_ci_{1}'.format(k, d) for k in measures_w_ci for d in ['left', 'right']] +
                            ['s1_frequency', 's2_frequency', 's1s2_frequency'])

        for k in abs_msr['cooc_freq']:
            csv_writer.writerow([k] +
                                [measure_dict[msr][k] for msr in measure_dict] +
                                [ci_dict[c][k][i] for c in ci_dict for i in [0, 1]] +
                                [abs_msr['suff_freq'][suff] for suff in k] + [abs_msr['cooc_freq'][k]])


def colloc_stats(right_parse_sign, suffix_boundary, mboundary, query_term="", faffix=""):
    measure_dict = dict(zip(measures, [dict() for m in measures]))
    ci_dict = dict(zip(measures_w_ci, [dict() for m in measures_w_ci]))
    abs_msr = {'suff_freq': defaultdict(int), 'cooc_freq': defaultdict(int)}

    # Tally suffixes and suffix collocates
    tally(query_term, right_parse_sign, suffix_boundary, mboundary, abs_msr)

    # Get number of suffix instances (size of sample)
    num_suffixes = sum(abs_msr['suff_freq'][s] for s in abs_msr['suff_freq'])

    # Get association measures
    calc_assoc_score(abs_msr, num_suffixes, measure_dict, ci_dict)

    # Save stats in files
    save_data(abs_msr, faffix, query_term, measure_dict, ci_dict)


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
