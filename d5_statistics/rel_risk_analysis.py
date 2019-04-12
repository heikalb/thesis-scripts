# -*- coding: UTF-8 -*-
import csv
import os
from collections import defaultdict


# Get the formulaicity proportion associated with verb types
def rr_rate(fpaths):
    save_rows = []

    for fpath in fpaths:
        with open(fpath, 'r') as f:
            rows = [r for r in csv.reader(f)][1:]

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
        save_rows.append([fpath.split('_')[2], rr_above_1/len(rows)])

    with open('rel_risk_rates.csv', 'w') as f:
        csv.writer(f).writerows(save_rows)


# Show the how many collocate pairs appear with how many verb types
def top_pairs(fpaths):
    pair_count_byverbs = defaultdict(int)

    # Tally verb type occurrences
    for fpath in fpaths:
        with open(fpath, 'r') as f:
            rows = [r for r in csv.reader(f)][1:]

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


# Find the trend of the RR of a pair across verbs
def cross_verb_trend(fpaths, target_pairs):
    target_rrs = {}
    stems = [fpath.split('_')[2] for fpath in fpaths]

    # Get pairs
    with open(fpaths[-1], 'r') as f:
        target_pairs = [r[0] for r in csv.reader(f)][1:]

    target_rrs = dict(zip(target_pairs, [defaultdict(lambda:'') for t in target_pairs]))

    """
    # Get RR of the target verbs in each file
    for tp in target_pairs:
        target_rrs[tp] = {}

        for fpath in fpaths:
            curr_stem = fpath.split('_')[2]

            with open(fpath, 'r') as f:
                curr_rr = [r for r in csv.reader(f) if r[0] == tp]

                if curr_rr:
                    target_rrs[tp][curr_stem] = curr_rr[0][1]
                else:
                    target_rrs[tp][curr_stem] = ''
    """

    # Get RR of the target verbs in each file
    for fpath in fpaths:
        curr_stem = fpath.split('_')[2]

        with open(fpath, 'r') as f:
            first_row = True

            for r in csv.reader(f):
                if first_row:
                    first_row = False
                    continue

                target_rrs[r[0]][curr_stem] = r[1]

    # Save data
    with open('rr_trend_of_pairs.csv', 'w') as f:
        csv.writer(f).writerow(['Pair'] + [s for s in stems])

        for tp in target_rrs:
            csv.writer(f).writerow([tp] + [target_rrs[tp][s] for s in stems])

    return


def main():
    data_dir = os.listdir('assoc_stats/')
    data_dir.sort()
    data_file_paths = [os.path.join('assoc_stats/', fp) for fp in data_dir]

    # rr_rate(data_file_paths)
    # tops = top_pairs(data_file_paths)
    trend_verbs = ["('Aor', 'While→Adv')", "('Aor', 'Cond')", "('Able→Verb', 'Aor')", "('Prog1', 'Past')"
                   , "('Pass→Verb', 'Aor')", "('Pass→Verb', 'Past')"]
    cross_verb_trend(data_file_paths, trend_verbs)


if __name__ == '__main__':
    main()
    exit(0)
