# -*- coding: UTF-8 -*-
"""
Display data for steps of analysis in Section 4.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import os
import math
import numpy
from collections import defaultdict
from scipy import stats


def freq_filter(rows):
    return [r for r in rows if float(r[12]) >= 100 and float(r[13]) >= 100]


def rr_ranges():
    """
    Display risk ratio by ranges for Table 10.
    """
    # Get risk ratios and risk ratio confidence intervals
    rr = [float(d[1]) for d in data]
    rr_ci = [float(d[8]) for d in data]

    # Pair up data with correct label
    measures = [(rr, 'Risk ratio'), (rr_ci, 'Risk ratio CI')]

    # Display ranges of data
    for measure in measures:
        # Divide data into ranges
        upto_1 = len([d for d in measure[0] if d <= 1])
        below_2 = len([d for d in measure[0] if 1 < d < 2])
        above_2 = len([d for d in measure[0] if 2 <= d])

        # Display ranges
        print(measure[1])
        print(f'RR below 1: {upto_1} ({upto_1 / len(measure[0])}%)')
        print(f'RR below 2: {below_2} ({below_2 / len(measure[0])}%)')
        print(f'RR above 2: {above_2} ({above_2 / len(measure[0])}%)')


def rr_ranges_by_register():
    """
    Show ranges of risk ratios by register for Table 12.
    """
    # Iterate by register. Use empty string for entire dataset
    for reg in ['', '_written', '_spoken']:
        # Get correct path to data file
        file_path = f'association_stats{reg}/000__association_stats{reg}.csv'

        # Get data
        with open(file_path, 'r') as f:
            reg_data = [r for r in csv.reader(f)][1:]
            reg_data = freq_filter(reg_data)

        # Get frequencies in ranges (type frequency)
        total = len(reg_data)
        up_to_1 = len([r for r in reg_data if float(r[1]) <= 1])
        more_than_1 = len([r for r in reg_data if float(r[1]) > 1])

        # Display ranges (type frequency)
        print(f'Pair types in {reg} register')
        print(f'Up to 1: {up_to_1} ({round(100*up_to_1/total)}%)')
        print(f'More than 1: {more_than_1} ({round(100*more_than_1/total)}%)')
        print('Total:', total, '\n')

        # Get frequencies in ranges (token frequency)
        total = sum([int(r[-3]) for r in reg_data])
        up_to_1 = sum([int(r[-3]) for r in reg_data if float(r[1]) <= 1])
        more_than_1 = sum([int(r[-3]) for r in reg_data if float(r[1]) > 1])

        # Display ranges (token frequency)
        print(f'Pair instances in {reg} register')
        print(f'Up to 1: {up_to_1} ({round(100*up_to_1/total)}%)')
        print(f'More than 1 {more_than_1} ({round(100*more_than_1/total)}%)')
        print('Total:', total, '\n')


def adjacency():
    """
    Display data related to risk ratio and suffix adjacency for Table 13.
    Run ANOVA on effect of adjacency for Section 4.1.
    """
    # Get collocate pairs with risk ratio above 1
    data_ = [row for row in data if float(row[1]) > 1]

    # Get adjacency frequencies
    def f(x): return [float(r[1]) for r in data_ if x(int(r[-2])/int(r[-3]))]

    adjacent = f(lambda x: x == 1)
    subadjacent = f(lambda x: 0 < x < 1)
    nonadjacent = f(lambda x: x == 0)

    # Display adjacent frequencies and related data
    def g(x, y): print(x, len(y), sum(y)/len(y), numpy.var(y), numpy.median(y))

    print('Pair frequency, average RR,variance, median')
    g('Adjacent:', adjacent)
    g('Subadjacent:', subadjacent)
    g('Nonadjacent:', nonadjacent)

    # Conduct tests on adjacency
    print('\n')
    print(stats.ttest_ind(adjacent, nonadjacent, equal_var=True))
    print(stats.ttest_ind(adjacent, nonadjacent, equal_var=False))
    print('Levene\'s test:', stats.levene(adjacent, subadjacent, nonadjacent))
    print('1-way ANOVA:', (stats.f_oneway(adjacent, subadjacent, nonadjacent)))
    print('Pearson correlation:', stats.pearsonr([float(r[1]) for r in data],
                                                 [int(r[-1]) for r in data]))


def asymmtery():
    """
    Display ratios of risk ratio to risk ratio reverse for Table 14.
    """
    # Get collocate pairs with risk ratio above 1
    data_ = [row for row in data if float(row[1]) > 1]

    # Get ratios
    def f(x): return max(float(x[1])/float(x[2]), float(x[2])/float(x[1]))

    atleast_2 = [f(d) for d in data_ if f(d) >= 2]
    atleast_2_types = [d[0] for d in data_ if f(d) >= 2]
    below_2 = [f(d) for d in data_ if f(d) < 2]

    # Display data
    print(len(atleast_2), min(atleast_2), max(atleast_2))
    print(len(below_2), min(below_2), max(below_2))

    for e in atleast_2_types:
        print(e)


def has_subordinate():
    """
    Count trigrams containing one of the subordinate suffixes for Section 4.2.
    """
    # Open data files
    with open('trigram/suffix_trigrams.txt', 'r') as f:
        trigram_lines = f.read().split('\n')

    # Count trigrams with a subordinate suffix
    subordinates = ['Inf2→Noun', 'PastPart→Noun', 'FutPart→Noun']
    num_has_subordinate = 0

    for trigram_line in trigram_lines:
        # Get information from trigram file line
        trigram, trigram_freq = trigram_line.split(') ')

        if any([suffix in trigram for suffix in subordinates]):
            num_has_subordinate += 1

    print('Number of trigrams with a subordinate marker: ', num_has_subordinate)


def test_normality():
    """
    Test the main risk ratio data for normality for Section 4.3.
    """
    # Get risk ratios
    data_ = [d[1] for d in data]

    # Run normality test
    print('Shapiro-Wilk test for normality:')
    print(stats.shapiro([math.log(float(d)) for d in data_]))


def integrity():
    """
    Display ranges of integrity ratios for Table 18.
    """
    # Get collocate pairs of different formulaicity
    all_pairs = data
    formulaic_pairs = [row for row in data if float(row[1]) > 1]
    nonformulaic_pairs = [row for row in data if float(row[1]) <= 1]

    # Iterate over different subsets of collocate pairs
    for subdataset in [all_pairs, formulaic_pairs, nonformulaic_pairs]:

        # For a given list of collocate pairs, return the number of collocate
        # pairs whose integrity ratio meet a threshold given by x().
        def f(x):
            return len([r for r in subdataset if x(float(r[-2])/float(r[-3]))])

        # Get frequencies of different integrity ratio categories
        exactly_1 = f(lambda x: x == 1)
        half = f(lambda x: 0.5 <= x < 1)
        below_half = f(lambda x: 0 < x < 0.5)
        zero = f(lambda x: x == 0)

        # Display data
        print(exactly_1, half, below_half, zero)
        print(exactly_1/len(subdataset), half/len(subdataset),
              below_half/len(subdataset), zero/len(subdataset))


def trigram_link_ratios():
    """
    Display ranges of trigram link ratios for Table 19.
    """
    # Get trigrams
    with open('trigram/suffix_trigrams.txt', 'r') as f:
        trigram_lines = f.read().split('\n')

    # Store risk ratio of suffix pairs
    data_ = dict(zip([r[0] for r in data if float(r[1]) > 1], [float(r[1]) for r in data if float(r[1]) > 1]))

    # Store risk ratios
    risk_ratios = []

    # Get risk ratios of stem-trigrams
    for trigram_line in trigram_lines:
        # Get information from trigram file line
        trigram = trigram_line.split(') ')[0]

        # Form tuples from trigram strings
        trigram = trigram[1:].split(', ')
        trigram = tuple([suffix[1:-1] for suffix in trigram])

        # Get constituent bigrams within the trigram
        bigrams = [(trigram[0], trigram[1]), (trigram[1], trigram[2])]

        # Get risk ratio of each bigram
        try:
            curr_rr = (data_[str(bigrams[0])], data_[str(bigrams[1])])

            if all([rr > 1 for rr in curr_rr]):
                risk_ratios.append(curr_rr)
        except KeyError:
            continue

    # Get ranges of risk ratio ratios
    def f(x): return len([r for r in risk_ratios
                          if x(min(r[0]/r[1], r[1]/r[0]))])

    rr_ratio_1 = f(lambda x: 0.9 <= x <= 1)
    rr_ratio_2 = f(lambda x: 0.5 <= x < 0.9)
    rr_ratio_3 = f(lambda x: 0.1 <= x < 0.5)
    rr_ratio_4 = f(lambda x: x < 0.1)

    # Display data
    print('0.9 ≤ x ≤ 1:', rr_ratio_1, rr_ratio_1/len(risk_ratios))
    print('0.5 ≤ x < 0.9:', rr_ratio_2, rr_ratio_2/len(risk_ratios))
    print('0.1 ≤ x < 0.5:', rr_ratio_3, rr_ratio_3/len(risk_ratios))
    print('x < 0.1:', rr_ratio_4, rr_ratio_4/len(risk_ratios))


def stem_trigram_formulas():
    """
    Tell how many stem-trigram pairs have a risk ratio above 1 for
    approximately page 62.
    """
    with open('trigram/stem_trigram_rr.csv', 'r') as f:
        data = [row for row in csv.reader(f)][1:]
        data = [r for r in data if float(r[4]) >= 100 and float(r[5]) >= 100]

    print(len([r for r in data if float(r[2]) > 1]))
    print(len(data))


def stem_by_trigram():
    """
    Tell how many verbs are associated with certain trigrams for Table 20.
    """
    with open('trigram/stem_trigram_rr.csv', 'r') as f:
        data = [row for row in csv.reader(f)][1:]
        data = [r for r in data if float(r[4]) >= 100 and float(r[5]) >= 100]

    above_1 = defaultdict(int)
    up_to_1 = defaultdict(int)
    num_hosting_verbs = defaultdict(int)
    risk_ratios = defaultdict(list)

    for row in data:
        trigram = row[1]
        risk_ratio = float(row[2])

        num_hosting_verbs[trigram] += 1
        risk_ratios[trigram].append(risk_ratio)

        if risk_ratio > 1:
            above_1[trigram] += 1
        if risk_ratio <= 1:
            up_to_1[trigram] += 1

    for trigram in above_1:
        print(trigram)

    print('\n')

    for trigram in above_1:
        print(up_to_1[trigram],
              '({0:.0%})'.format(up_to_1[trigram]/num_hosting_verbs[trigram]))

    print('\n')

    for trigram in above_1:
        print(above_1[trigram],
              '({0:.0%})'.format(above_1[trigram] / num_hosting_verbs[trigram]))

    print('\n')

    for trigram in above_1:
        print(f'{round(math.log(min(risk_ratios[trigram]), 2), 2)}'
              f'  -  {round(math.log(max(risk_ratios[trigram]), 2), 2)}')


# Get the formula frequency and proportion associated with verb types
def rr_dist(fpaths=[], save_file_name='rr_dist_by_verbs.csv'):
    save_rows = []

    for fpath in fpaths:
        with open(fpath, 'r') as f:
            rows = [r for r in csv.reader(f)][1:]

        if not rows:
            continue

        f_freq = sum([int(r[-1]) for r in rows if float(r[1]) > 1])
        num_f_types = len([r for r in rows if float(r[1]) > 1])
        inst_sum = sum([int(r[-1]) for r in rows])
        type_sum = len([r for r in rows])
        save_rows.append([fpath.split('_')[2], f_freq, f_freq/inst_sum,
                          num_f_types, num_f_types/type_sum])

    with open(save_file_name, 'w') as f:
        row_1 = ['verb_lemma', 'formula_freq', 'formula_freq_norm',
                 'num_formula', 'formula_prop']

        csv.writer(f).writerow(row_1)
        csv.writer(f).writerows(save_rows)


# Show how many collocate pairs appear with how many verb types
def top_pairs(fpaths):
    pair_count_byverbs = defaultdict(int)
    overall_rr = dict()

    # Tally verb type occurrences
    for fpath in fpaths:
        with open(fpath, 'r') as f:
            rows = [r for r in csv.reader(f)][1:]

        for r in rows:
            pair_count_byverbs[r[0]] += 1

            if '000' in fpath:
                overall_rr[r[0]] = r[1]

    # Display number of collocate pairs in different ranges of verb type freq.
    for i in range(8):
        pairs = [p for p in pair_count_byverbs
                 if i*100 <= pair_count_byverbs[p] < (i+1)*100]

        print(i*100, (i+1)*100)
        print(len(pairs), '\n')

    # Get the most verb-frequent collocate pairs
    keys = [k for k in pair_count_byverbs]
    keys.sort(reverse=True, key=lambda x: pair_count_byverbs[x])

    for p in keys[:81]:
        print(f'{p}\t\t\t\t{pair_count_byverbs[p]}\t\t\t\t{overall_rr[p]}')

    return keys[:20]


# Find the trend of the RR of a pair across verbs
def cross_verb_trend(fpaths):
    # Get all pairs in whole dataset
    with open(fpaths[-1], 'r') as f:
        target_pairs = [r[0] for r in csv.reader(f)][1:]

    target_rrs = dict(zip(target_pairs,
                          [defaultdict(lambda:'') for t in target_pairs]))

    # Get RR of collocate pairs across verb files
    for fpath in fpaths:
        curr_stem = fpath.split('_')[2]

        with open(fpath, 'r') as f:
            for r in [r_ for r_ in csv.reader(f)][1:]:
                target_rrs[r[0]][curr_stem] = r[1]

    # Save data
    with open('cross_verb_trends.csv', 'w') as f:
        stems = [fpath.split('_')[2] for fpath in fpaths]
        row_1 = ['Pair'] + [s for s in stems] + ['Verb_type_frequency']
        rows = [[k] + [target_rrs[k][s] for s in stems] +
                [len([s for s in target_rrs[k] if target_rrs[k][s]]) - 1]
                for k in target_rrs]

        csv.writer(f).writerow(row_1)
        csv.writer(f).writerows(rows)


def formulas():
    for r in data:
        if int(r[-3]) == int(r[-2] or int(r[-4]) == int(r[-2])):
            print(r[0])


if __name__ == '__main__':
    data_dir = os.listdir('association_stats/')
    data_dir.sort()
    data_files = [os.path.join('association_stats/', fp) for fp in data_dir]

    with open(f'association_stats/000__association_stats.csv', 'r') as f:
        data = [row for row in csv.reader(f)][1:]
        data = freq_filter(data)

    # rr_ranges()
    # rr_ranges_by_register()
    # adjacency()
    # asymmtery()
    # has_subordinate()
    # test_normality()
    # integrity()
    trigram_link_ratios()
    # stem_trigram_formulas()
    # stem_by_trigram()
    # rr_dist(data_files)
    # tops = top_pairs(data_files)
    # cross_verb_trend(data_files)
    # test_normality('association_stats/000__association_stats.csv')
    # formulas()

    exit(0)
