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
def tally(query_term, right_sign, suff_boundary, mboundary, freq, bound=-1, register=''):
    for parse in parses:
        # Skip parses for a different stem or wrong parses
        if query_term not in parse[0] or right_sign not in parse[0] or (register and register != parse[2]):
            continue

        # Get suffixes, exclude stems. Collapse allomorphs. Remove unneeded suffixes the parser introduced
        suffixes = re.split(suff_boundary, parse[1])[1:]
        suffixes = remove_forbidden_suffixes(suffixes)
        suffixes = [re.sub(mboundary, '', s) for s in suffixes]

        # Count suffix (co)occurrences
        for i in range(len(suffixes)):
            freq['suff'][suffixes[i]] += 1

            d = 0
            for j in range(i + 1, len(suffixes)):
                curr_pair = (suffixes[i], suffixes[j])
                freq['cooc'][curr_pair] += 1
                d += 1

                if bound != -1 and d >= bound:
                    break

    print(query_term, sum([freq['cooc'][k] for k in freq['cooc']]))

# Remove unneeded suffixes
def remove_forbidden_suffixes(suffixes):
    ret = []
    i = 0
    
    for s in suffixes:
        # if not ('Zero' in s or ('A3sg' in s and i < len(suffixes) - 1)):
        #    ret.append(s)
        if ':' in s or ('A3sg' == s and i == len(suffixes)-1):
            ret.append(s)
        i += 1

    return ret


# Get various association score for collocate pairs
def calc_assoc_score(freq, num_suffixes, measure_dict, ci_dict):
    for k in freq['cooc']:
        m1, m2 = k

        for msr in measures:
            args = [freq['suff'][m1], freq['suff'][m2], freq['cooc'][k], num_suffixes, m1, m2, freq['cooc']]
            stat = measure_funct[msr](*args)

            if type(stat) == tuple:
                measure_dict[msr][k] = stat[0]
                ci_dict[msr][k] = stat[1]
            else:
                measure_dict[msr][k] = stat


# Save frequency data and association score in files
def save_data(freq, faffix, dir_affix, query_term, measure_dict, ci_dict):
    # Save absolute frequency data
    for msr in freq:
        if not os.path.isdir('{0}{1}'.format(msr, dir_affix)):
            os.mkdir('{0}{1}'.format(msr, dir_affix))

        with open('{0}{1}/{2}_{3}_{0}{4}.csv'.format(msr, dir_affix, faffix, query_term, dir_affix), 'w') as f:
            csv_writer = csv.writer(f)

            for k in freq[msr]:
                csv_writer.writerow([k, freq[msr][k]])

    # Save association measures data
    if not os.path.isdir('assoc_stats{0}'.format(dir_affix)):
        os.mkdir('assoc_stats{0}'.format(dir_affix))

    with open('assoc_stats{0}/{1}_{2}_assoc_stats{3}.csv'.format(dir_affix, faffix, query_term, dir_affix), 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["collocate_pair"] + [m for m in measures] +
                            ['{0}_ci_{1}'.format(k, d) for k in measures_w_ci for d in ['left', 'right']] +
                            ['s1_frequency', 's2_frequency', 's1s2_frequency'])

        for k in freq['cooc']:
            csv_writer.writerow([k] + [measure_dict[msr][k] for msr in measure_dict] +
                                [ci_dict[c][k][i] for c in ci_dict for i in [0, 1]] +
                                [freq['suff'][suff] for suff in k] + [freq['cooc'][k]])


def colloc_stats(right_sign, suff_boundary, mboundary, query_term="", faffix="", dir_affix='', register='', bound=-1):
    measure_dict = dict(zip(measures, [dict() for m in measures]))
    ci_dict = dict(zip(measures_w_ci, [dict() for m in measures_w_ci]))
    freq = {'suff': defaultdict(int), 'cooc': defaultdict(int)}

    # Tally suffixes and suffix collocates
    tally(query_term, right_sign, suff_boundary, mboundary, freq, bound, register)

    # Get number of suffix instances (size of sample)
    num_suffixes = sum(freq['suff'][s] for s in freq['suff'])

    # Get association measures
    calc_assoc_score(freq, num_suffixes, measure_dict, ci_dict)

    # Save stats in files
    save_data(freq, faffix, dir_affix, query_term, measure_dict, ci_dict)


if __name__ == "__main__":
    # Get verb parses
    with open('../d4_parse/verb_parses.txt', 'r') as f:
        parses = [p.split() for p in f.read().split('\n')]

    # Get query terms
    query_terms = [""] + open('../d0_prep_query_terms/freq_dict_verbs.txt', 'r').read().split('\n')
    # Data not available for this one
    query_terms.remove('savrul')
    # File indexes
    f_i = [""] + [('00'+str(i))[-3:] for i in range(len(query_terms))]

    # Get statistics for each verb type
    for qt in query_terms:
        print(qt)
        colloc_stats('Verb', r'[\|\+]', r'.*:', qt, f_i[query_terms.index(qt)])
        # colloc_stats('Verb', r'[\|\+]', r'.*:', qt, f_i[query_terms.index(qt)], '_written', 'w')
        # colloc_stats('Verb', r'[\|\+]', r'.*:', qt, f_i[query_terms.index(qt)], '_spoken', 's')

    exit(0)
