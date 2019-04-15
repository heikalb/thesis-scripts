# -*- coding: UTF-8 -*-
import csv
import os
from collections import defaultdict


# Get the formula frequency and proportion associated with verb types
def rr_dist(fpaths=[], save_file_name='rr_dist_by_verbs.csv'):
    save_rows = []

    for fpath in fpaths:
        with open(fpath, 'r') as f:
            rows = [r for r in csv.reader(f)][1:]

        if not rows:
            continue

        abs_freq = sum([int(r[-1]) for r in rows if float(r[1]) > 1])
        proportion = len([r for r in rows if float(r[1]) > 1])
        save_rows.append([fpath.split('_')[2], abs_freq, abs_freq/len(rows), proportion, proportion/len(rows)])

    with open(save_file_name, 'w') as f:
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
        csv.writer(f).writerow(['Pair'] + [s for s in stems])
        csv.writer(f).writerows([[k] + [target_rrs[k][s] for s in stems] for k in target_rrs])


def main():
    data_dir = os.listdir('assoc_stats/')
    data_dir.sort()
    data_file_paths = [os.path.join('assoc_stats/', fp) for fp in data_dir]

    rr_dist(data_file_paths)
    # tops = top_pairs(data_file_paths)
    # cross_verb_trend(data_file_paths)


if __name__ == '__main__':
    main()
    exit(0)
