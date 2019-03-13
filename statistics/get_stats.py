"""
Get various collocation statistics from the corpus
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""

import csv
from collections import defaultdict
import re
import colloc_measures as cm

measures = ['mutual_information', 't_score', 'dice_coefficient', 'chi_squared']
measure_funct = dict(zip(measures, [cm.mutual_info, cm.t_score, cm.dice_coeff, cm.chi_squared]))
measure_dict = dict(zip(measures, [dict() for m in measures]))


def colloc_stats(right_parse_sign, suffix_boundary, mboundary, key_separator, query_term=""):
    # Open file of parses
    parses = open('../parse/parses_verbs.txt', 'r').read().split('\n')
    parses = [p.split() for p in parses]

    # Stats
    suff_freq = defaultdict(int)
    cooc_freq = defaultdict(int)
    mutual_infos = {}
    t_scores = {}
    dice_coeff = {}
    chi_squared = {}

    # Go through parses
    for parse in parses:
        # Skip parses for a different stem or wrong parses
        if query_term not in parse[0] or right_parse_sign not in parse[0]:
            continue

        # Get suffixes, exclude stems
        suffixes = re.split(suffix_boundary, parse[1])[1:]

        # Collapse allomorphs
        suffixes = [re.sub(mboundary, '', s) for s in suffixes]

        # Count suffix (co)occurrences
        for i in range(len(suffixes)):
            # Updata single suffix count
            suff_freq[suffixes[i]] += 1

            # Update count for co-occurring pairs
            for j in range(i + 1, len(suffixes)):
                curr_key = '{0}{1}{2}'.format(suffixes[i], key_separator, suffixes[j])
                cooc_freq[curr_key] += 1

    num_suffixes = sum(suff_freq[s] for s in suff_freq)

    # Get association measures
    for k in cooc_freq:
        m1, m2 = k.split(key_separator)

        for msr in measures:
            args = [suff_freq[m1], suff_freq[m2], cooc_freq[k], num_suffixes, m1, m2, cooc_freq]
            measure_dict[msr][k] = (measure_funct[msr](*args), suff_freq[m1], suff_freq[m2])

    """
    # Get association measures
    for k in cooc_freq:
        mutual_infos[k] = (cm.mutual_info(suff_freq[m1], suff_freq[m2], cooc_freq[k], num_suffixes),
                           suff_freq[m1], suff_freq[m2])

        t_scores[k] = (cm.t_score(suff_freq[m1], suff_freq[m2], cooc_freq[k], num_suffixes),
                       suff_freq[m1], suff_freq[m2])

        dice_coeff[k] = (cm.dice_coeff(suff_freq[m1], suff_freq[m2], cooc_freq[k]),
                         suff_freq[m1], suff_freq[m2])

        chi_squared[k] = (cm.chi_squared(suff_freq[m1], suff_freq[m2], cooc_freq[k], num_suffixes, m1, m2, cooc_freq),
                          suff_freq[m1], suff_freq[m2])
    """

    # Save data
    with open('cooccurrence_count/cooccurrence_count_{0}.csv'.format(query_term), 'w') as f:
        csv_writer = csv.writer(f)

        for k in cooc_freq:
            csv_writer.writerow([k, cooc_freq[k]])

    with open('suffix_count/suffix_count_{0}.csv'.format(query_term), 'w') as f:
        csv_writer = csv.writer(f)

        for k in suff_freq:
            csv_writer.writerow([k, suff_freq[k]])

    for msr in measures:
        with open('{0}/{0}_{1}.csv'.format(msr, query_term), 'w') as f:
            csv_writer = csv.writer(f)

            for k in measure_dict[msr]:
                csv_writer.writerow([k, measure_dict[msr][k][0], measure_dict[msr][k][1], measure_dict[msr][k][2]])

    """
    with open('mutual_info/mutual_info_{0}.csv'.format(query_term), 'w') as f:
        csv_writer = csv.writer(f)

        for k in mutual_infos:
            csv_writer.writerow([k, mutual_infos[k][0], mutual_infos[k][1], mutual_infos[k][2]])

    with open('t_scores/t_scores_{0}.csv'.format(query_term), 'w') as f:
        csv_writer = csv.writer(f)

        for k in t_scores:
            csv_writer.writerow([k, t_scores[k][0], t_scores[k][1], t_scores[k][2]])

    with open('dice_coeff/dice_coeff_{0}.csv'.format(query_term), 'w') as f:
        csv_writer = csv.writer(f)

        for k in dice_coeff:
            csv_writer.writerow([k, dice_coeff[k][0], dice_coeff[k][1], dice_coeff[k][2]])

    with open('chi_squared/chi_squared_{0}.csv'.format(query_term), 'w') as f:
        csv_writer = csv.writer(f)

        for k in chi_squared:
            csv_writer.writerow([k, chi_squared[k][0], chi_squared[k][1], chi_squared[k][2]])
    """


def main():
    query_terms = [""] + open('../data/query_terms.txt', 'r').read().split('\n')

    for qt in query_terms:
        colloc_stats(right_parse_sign='Verb', suffix_boundary=r'[\|\+]', mboundary=r'.*:',
                     key_separator='__', query_term=qt)


if __name__ == "__main__":
    main()
    exit(0)
