# -*- coding: UTF-8 -*-
import csv
import os
from collections import defaultdict
import math
import numpy
from scipy import stats


def rr_ranges(fname):
    with open(fname, 'r') as f:
        data = [r[8] for r in csv.reader(f)][1:]

    data = [float(d) for d in data]
    upto_1 = len([d for d in data if d <= 1])
    below_2 = len([d for d in data if 1 < d < 2])
    above_2 = len([d for d in data if 2 <= d])

    print(f'RR below 1: {upto_1} ({upto_1/len(data)}%)')
    print(f'RR below 2: {below_2} ({below_2/len(data)}%)')
    print(f'RR above 2: {above_2} ({above_2/len(data)}%)')


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
        save_rows.append([fpath.split('_')[2], f_freq, f_freq/inst_sum, num_f_types, num_f_types/type_sum])

    with open(save_file_name, 'w') as f:
        csv.writer(f).writerow(['verb_lemma', 'formula_freq', 'formula_freq_norm', 'num_formula', 'formula_prop'])
        csv.writer(f).writerows(save_rows)


# Show the how many collocate pairs appear with how many verb types
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

    # Display number of collocate pairs for different ranges of verb type numbers
    for i in range(8):
        pairs = [p for p in pair_count_byverbs if i*100 <= pair_count_byverbs[p] < (i+1)*100]
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

    target_rrs = dict(zip(target_pairs, [defaultdict(lambda:'') for t in target_pairs]))

    # Get RR of collocate pairs across verb files
    for fpath in fpaths:
        curr_stem = fpath.split('_')[2]

        with open(fpath, 'r') as f:
            for r in [r_ for r_ in csv.reader(f)][1:]:
                target_rrs[r[0]][curr_stem] = r[1]

    # Save data
    with open('cross_verb_trends.csv', 'w') as f:
        stems = [fpath.split('_')[2] for fpath in fpaths]
        csv.writer(f).writerow(['Pair'] + [s for s in stems] + ['Verb_type_frequency'])
        csv.writer(f).writerows([[k] + [target_rrs[k][s] for s in stems] +
                                 [len([s for s in target_rrs[k] if target_rrs[k][s]]) - 1] for k in target_rrs])


def test_normality(fpath):
    with open(fpath, 'r') as f:
        data = [r[1] for r in csv.reader(f)][1:]
        data = [math.log(float(d)) for d in data]

    print('Shapiro-Wilk test for normality:')
    print(stats.shapiro(data))


def register():
    for reg in ['', '_written', '_spoken']:
        with open(f'association_stats{reg}/000__association_stats{reg}.csv', 'r') as f:
            data = [r for r in csv.reader(f)][1:]

        total = len(data)
        up_to_1 = len([r for r in data if float(r[1]) <= 1])
        more_than_1 = len([r for r in data if float(r[1]) > 1])

        print(f'Pair types in {reg} register')
        print(f'Up to 1: {up_to_1} ({round(100*up_to_1/total)}%)')
        print(f'More than 1: {more_than_1} ({round(100*more_than_1/total)}%)')
        print(total, '\n')

        total = sum([int(r[-3]) for r in data])
        up_to_1 = sum([int(r[-3]) for r in data if float(r[1]) <= 1])
        more_than_1 = sum([int(r[-3]) for r in data if float(r[1]) > 1])

        print(f'Pair instances in {reg} register')
        print(f'Up to 1: {up_to_1} ({round(100*up_to_1/total)}%)')
        print(f'More than 1 {more_than_1} ({round(100*more_than_1/total)}%)')
        print(total, '\n')


def adjacency():
    with open(f'association_stats/000__association_stats.csv', 'r') as f:
        data = [r for r in csv.reader(f)][1:]

    # adjacent = [math.log(float(r[1])) for r in data if int(r[-1])/int(r[-2]) > 0]
    adjacent = [math.log(float(r[1])) for r in data if int(r[-2])/int(r[-3]) == 1 if float(r[1]) > 1]
    sub_adjacent = [math.log(float(r[1])) for r in data if 0 < int(r[-2])/int(r[-3]) < 1 if float(r[1]) > 1]
    nonadjacent = [math.log(float(r[1])) for r in data if int(r[-2])/int(r[-3]) == 0 if float(r[1]) > 1]

    print('Pair frequency, average log RR,variance, standard deviation')
    print('Adjacent:', len(adjacent), sum(adjacent) / len(adjacent), numpy.var(adjacent), numpy.std(adjacent))
    print('Sub Adjacent:', len(sub_adjacent), sum(sub_adjacent) / len(sub_adjacent), numpy.var(sub_adjacent), numpy.std(sub_adjacent))
    print('Non adjacent', len(nonadjacent), sum(nonadjacent) / len(nonadjacent), numpy.var(nonadjacent), numpy.std(nonadjacent))
    # print(stats.ttest_ind(adjacent, nonadjacent, equal_var=True))
    # print(stats.ttest_ind(adjacent, nonadjacent, equal_var=False))
    print('Levene\'s test:', stats.levene(adjacent, sub_adjacent, nonadjacent))
    print('One way ANOVA:',(stats.f_oneway(adjacent, sub_adjacent, nonadjacent)))
    print('Pearson correlation:', stats.pearsonr([float(r[1]) for r in data], [int(r[-1]) for r in data]))


def formulas():
    with open(f'association_stats/__association_stats.csv', 'r') as f:
        data = [r for r in csv.reader(f)][1:]

    for r in data:
        # if int(r[-3]) >= 100 and int(r[-4]) >= 100:
        if int(r[-3]) == int(r[-2] or int(r[-4]) == int(r[-2])):
            print(r[0])


def main():
    data_dir = os.listdir('association_stats/')
    data_dir.sort()
    data_file_paths = [os.path.join('association_stats/', fp) for fp in data_dir]

    # rr_ranges('association_stats/000__association_stats.csv')
    # rr_dist(data_file_paths)
    # tops = top_pairs(data_file_paths)
    # cross_verb_trend(data_file_paths)
    # test_normality('association_stats/__association_stats.csv')
    # register()
    # adjacency()
    # formulas()


if __name__ == '__main__':
    main()
    exit(0)
