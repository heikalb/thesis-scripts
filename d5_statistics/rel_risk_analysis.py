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
        rr_below_1 = len([r for r in rows if float(r[1]) <= 1])
        left_ci_above_1 = len([r for r in rows if float(r[2]) > 1])
        left_ci_below_1 = len([r for r in rows if float(r[2]) <= 1])
        rr_above_ci_below = len([r for r in rows if float(r[1]) > 1 and float(r[2]) <= 1])
        rr_above_ci_above = len([r for r in rows if float(r[1]) > 1 and float(r[2]) > 1])
        save_rows.append([stem, rr_above_ci_above/len(rows)])

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



def top_pairs(fpaths):
    pair_count_byverbs = defaultdict(int)

    for fpath in fpaths:
        with open(os.path.join(fpath), 'r') as f:
            rows = [r for r in csv.reader(f)]

        curr_pairs = [r[0] for r in rows if float(r[1]) > 1 and float(r[2]) > 1]

        for p in curr_pairs:
            pair_count_byverbs[p] += 1

    top_pairs = [p for p in pair_count_byverbs if pair_count_byverbs[p] >= 600]
    print(len(top_pairs))

    top_pairs = [p for p in pair_count_byverbs if 500 <= pair_count_byverbs[p] < 600]
    print(len(top_pairs))

    top_pairs = [p for p in pair_count_byverbs if 400 <= pair_count_byverbs[p] < 500]
    print(len(top_pairs))

    top_pairs = [p for p in pair_count_byverbs if 300 <= pair_count_byverbs[p] < 400]
    print(len(top_pairs))

    top_pairs = [p for p in pair_count_byverbs if 200 <= pair_count_byverbs[p] < 300]
    print(len(top_pairs))

    top_pairs = [p for p in pair_count_byverbs if 100 <= pair_count_byverbs[p] < 200]
    print(len(top_pairs))

    top_pairs = [p for p in pair_count_byverbs if pair_count_byverbs[p] < 100]
    print(len(top_pairs))
    exit()

    top_pairs.sort(reverse=True, key=lambda x: pair_count_byverbs[x])

    for p in top_pairs[:20]:
        print(p + '\t'*4, pair_count_byverbs[p])
    return top_pairs[:20]


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
            print(r, ranks[pair][r], end='   ')
        print('\n')

    return


def top_pair_trend_(fpaths, top_pairs):
    pair_rr = {}

    for fpath in fpaths:
        with open(os.path.join(fpath), 'r') as f:
            rows = [r for r in csv.reader(f)]

        for r in rows:
            if r[0] not in pair_rr:
                pair_rr[r[0]] = []

            pair_rr[r[0]].append(r[1])

    for p in pair_rr:
        print(p)
        for s in pair_rr[p]:
            print(s, end=' ')
        print('\n')

    return


def main():
    data_dir = os.listdir('relative_risk/')
    data_dir.sort()
    data_file_paths = [os.path.join('relative_risk/', fp) for fp in data_dir]

    #rr_rate(data_file_paths)
    tops = top_pairs(data_file_paths)
    #top_pair_trend_(data_file_paths, tops)
    #top_pair_trend(data_file_paths, tops)



if __name__ == '__main__':
    main()
    exit(0)