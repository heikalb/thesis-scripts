# -*- coding: UTF-8 -*-
import csv
import os
from collections import defaultdict


def rr_rate(fpaths):
    save_rows = []

    for fpath in fpaths:
        print(fpath)
        with open(os.path.join(fpath), 'r') as f:
            rows = [r for r in csv.reader(f)]

        stem = fpath.split('_')[2]

        if not rows:
            continue

        rr_above_1 = len([r for r in rows if float(r[1]) > 1])
        """
        rr_below_1 = len([r for r in rows if float(r[1]) <= 1])
        left_ci_above_1 = len([r for r in rows if float(r[2]) > 1])
        left_ci_below_1 = len([r for r in rows if float(r[2]) <= 1])
        rr_above_ci_below = len([r for r in rows if float(r[1]) > 1 and float(r[2]) <= 1])
        rr_above_ci_above = len([r for r in rows if float(r[1]) > 1 and float(r[2]) > 1])
        """
        save_rows.append([stem, rr_above_1/len(rows)])

    with open('rel_risk_rates.csv', 'w') as f:
        csv.writer(f).writerows(save_rows)


def rr_rate_across_verbs(fpaths):
    save_rows = []
    pair_stats = {}

    for fpath in fpaths:
        with open(os.path.join(fpath), 'r') as f:
            rows = [r for r in csv.reader(f)]

        for r in rows:
            if r[0] not in pair_stats:
                pair_stats[r[0]] = []


# Show the how many collocate pairs appearr in how many verb types
def top_pairs(fpaths):
    pair_count_byverbs = defaultdict(int)

    # Tally verb type occurrences
    for fpath in fpaths:
        with open(os.path.join(fpath), 'r') as f:
            rows = [r for r in csv.reader(f)]

        curr_pairs = [r[0] for r in rows if float(r[1]) > 1]

        for p in curr_pairs:
            pair_count_byverbs[p] += 1

    # Display number of collocate pairs for different ranges of verb type numbers
    for i in range(8):
        pairs = [p for p in pair_count_byverbs if i*100 <= pair_count_byverbs[p] < (i+1)*100]
        print(i*100, (i+1)*100)
        print(len(pairs), '\n')

    # Get the most verb-frequent collocate pairs
    keys = [k for k in pair_count_byverbs]
    keys.sort(reverse=True, key=lambda x: pair_count_byverbs[x])

    for p in keys[:81]:
        print(p + '\t'*4, pair_count_byverbs[p])

    return keys[:20]


def top_pair_trend(fpaths, top_pairs):
    verb_columns = {}
    ranks = {}

    for fpath in fpaths:
        with open(os.path.join(fpath), 'r') as f:
            rows = [r for r in csv.reader(f)]

        curr_pairs = [r for r in rows if float(r[1]) > 1 and float(r[2]) > 1]
        curr_pairs.sort(reverse=True, key=lambda x: x[1])
        curr_pairs = [r[0] for r in curr_pairs]
        verb_columns[fpath.split('_')[2]] = curr_pairs

    for tp in top_pairs:
        ranks[tp] = {}
        for v in verb_columns:
            try:
                ranks[tp][v] = verb_columns[v].index(tp)
            except:
                continue

    for pair in ranks:
        print(pair)
        for r in ranks[pair]:
            print(r, ranks[pair][r])
        print('\n')

    return


# Find the trend of the RR of a pair across verbs
def cross_verb_trend(fpaths, target_pairs):
    target_rrs = {}
    stems = [fpath.split('_')[2] for fpath in fpaths]

    # Get RR of the target verbs in each file
    for tp in target_pairs:
        target_rrs[tp] = {}

        for fpath in fpaths:
            curr_stem = fpath.split('_')[2]

            with open(os.path.join(fpath), 'r') as f:
                curr_rr = [r for r in csv.reader(f) if r[0] == tp]

                if curr_rr:
                    target_rrs[tp][curr_stem] = curr_rr[0][1]
                else:
                    target_rrs[tp][curr_stem] = ''

    # Save data
    with open('rr_trend_of_specific_pairs.csv', 'w') as f:
        csv.writer(f).writerow(['Pair'] + [s for s in stems])

        for tp in target_rrs:
            csv.writer(f).writerow([tp] + [target_rrs[tp][s] for s in target_rrs[tp]])

    return


def main():
    data_dir = os.listdir('relative_risk/')
    data_dir.sort()
    data_file_paths = [os.path.join('relative_risk/', fp) for fp in data_dir]

    rr_rate(data_file_paths)
    # tops = top_pairs(data_file_paths)
    # top_pair_trend_(data_file_paths, tops)
    # top_pair_trend(data_file_paths, tops)
    trend_verbs = ["('Aor', 'While→Adv')", "('Aor', 'Cond')", "('Able→Verb', 'Aor')", "('Prog1', 'Past')"
                   , "('Pass→Verb', 'Aor')", "('Pass→Verb', 'Past')"]
    cross_verb_trend(data_file_paths, trend_verbs)


if __name__ == '__main__':
    main()
    exit(0)
