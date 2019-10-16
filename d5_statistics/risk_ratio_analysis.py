# -*- coding: UTF-8 -*-
"""
Display data for steps of analysis in Section 4.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import numpy
from scipy import stats
import math
from collections import defaultdict


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

        # Get data, filter out low frequency pairs
        with open(file_path, 'r') as f:
            reg_data = [r for r in csv.reader(f)][1:]
            reg_data = [r for r in reg_data if float(r[12]) >= 100
                        and float(r[13]) >= 100]

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

        # Update count
        if any([suffix in trigram for suffix in subordinates]):
            num_has_subordinate += 1

    # Display data
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
    collocate_pairs = [r[0] for r in data if float(r[1]) > 1]
    risk_ratios = [float(r[1]) for r in data if float(r[1]) > 1]
    data_ = dict(zip(collocate_pairs, risk_ratios))

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
    Tell how many stem-trigram pairs have a risk ratio above 1 for Section 4.4.
    """
    # Get stem-trigram pairs
    with open('trigram/stem_trigram_rr.csv', 'r') as f:
        data = [row for row in csv.reader(f)][1:]
        data = [r for r in data if float(r[4]) >= 100 and float(r[5]) >= 100]

    # Count stem-trigram pairs with risk ratio above 1
    num_above_1 = len([r for r in data if float(r[2]) > 1])

    # Display data
    print('Stem-trigram pairs with risk ratio above 1:', num_above_1)
    print('Total number of stem-trigram pairs', len(data))


def stem_by_trigram():
    """
    Tell how many verbs are associated with certain trigrams for Table 20.
    """
    # Get stem-trigram pairs
    with open('trigram/stem_trigram_rr.csv', 'r') as f:
        data = [row for row in csv.reader(f)][1:]
        data = [r for r in data if float(r[4]) >= 100 and float(r[5]) >= 100]

    # Categories of association
    above_1 = defaultdict(int)
    up_to_1 = defaultdict(int)
    num_hosting_verbs = defaultdict(int)
    risk_ratios = defaultdict(list)

    # Get frequencies
    for row in data:
        trigram = row[1]
        risk_ratio = float(row[2])

        num_hosting_verbs[trigram] += 1
        risk_ratios[trigram].append(risk_ratio)

        if risk_ratio > 1:
            above_1[trigram] += 1
        if risk_ratio <= 1:
            up_to_1[trigram] += 1

    # Display data
    # Display trigrams
    for trigram in above_1:
        print(trigram)

    # Display absolute and relative frequencies
    for trigram in above_1:
        print(up_to_1[trigram],
              '({0:.0%})'.format(up_to_1[trigram]/num_hosting_verbs[trigram]))

    for trigram in above_1:
        print(above_1[trigram],
              '({0:.0%})'.format(above_1[trigram] / num_hosting_verbs[trigram]))

    # Display range of log risk ratio for above 1 category
    for trigram in above_1:
        print(f'{round(math.log(min(risk_ratios[trigram]), 2), 2)}'
              f'  -  {round(math.log(max(risk_ratios[trigram]), 2), 2)}')


if __name__ == '__main__':
    # Get data, filter out low frequency pairs
    with open(f'association_stats/000__association_stats.csv', 'r') as f:
        data = [row for row in csv.reader(f)][1:]
        data = [r for r in data if float(r[12]) >= 100 and float(r[13]) >= 100]

    # Run analysis
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

    exit(0)
