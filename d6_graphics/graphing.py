import matplotlib.pyplot as pyplot
import csv
import math
from collections import defaultdict


def meep(title='', xlabel='', ylabel='', fname='', xticks=0, xlim=0, ylim=0, dim=(12, 9)):
    pyplot.gcf().set_size_inches(dim[0], dim[1])
    pyplot.grid(axis='y', alpha=0.5)
    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)

    if xlim:
        pyplot.xlim(xlim[0], xlim[1])

    if ylim:
        pyplot.ylim(ylim[0], ylim[1])

    if xticks:
        pyplot.xticks(xticks, rotation=90)

    pyplot.tight_layout()
    pyplot.savefig(fname)
    pyplot.close()


def plot_rr():
    with open('../d5_statistics/assoc_stats/__assoc_stats.csv', 'r') as f:
        data = [r[1] for r in csv.reader(f)][1:]

    bin_edges = [0.5*i for i in range(36)]
    data = [round(float(e), 2) for e in data]
    n, bins, patches = pyplot.hist(data, bins=bin_edges, histtype='bar', edgecolor='w', alpha=0.8)

    meep('Histogram of relative risks', 'Relative risk', 'Number of collocate pairs', 'RR.png', [1*i for i in range(18)])


def plot_logrr():
    with open('../d5_statistics/assoc_stats/__assoc_stats.csv', 'r') as f:
        data = [r[1] for r in csv.reader(f)][1:]

    data = [round(math.log(float(e)), 2) for e in data]
    n, bins, patches = pyplot.hist(data, bins=[i*0.5 for i in range(-16, 24)], histtype='bar', edgecolor='w', alpha=0.8)
    meep('Histogram of log relative risks', 'Log relative risk', 'Number of collocate pairs', 'RR_log.png',
         [i for i in range(-8, 12)])


def plot_rrci():
    with open('../d5_statistics/assoc_stats/__assoc_stats.csv', 'r') as f:
        data = [r[-5] for r in csv.reader(f)][1:]

    bin_edges = [0.5 * i for i in range(36)]
    data = [round(float(e), 2) for e in data]
    n, bins, patches = pyplot.hist(data, bins=bin_edges, histtype='bar', edgecolor='w', alpha=0.8)
    meep('Histogram of relative risks', 'Relative risk', 'Number of collocate pairs', 'RR_ci.png',
         [1*i for i in range(18)], (0, 20))


def plot_register():
    for reg in ['spoken', 'written']:
        with open('../d5_statistics/assoc_stats_{0}/__assoc_stats_{0}.csv'.format(reg), 'r') as f:
            data = [r[1] for r in csv.reader(f)][1:]

        bin_edges = [0.5*i for i in range(36)]
        data = [round(float(e), 2) for e in data]
        n, bins, patches = pyplot.hist(data, bins=bin_edges, histtype='bar', edgecolor='w', alpha=0.8)
        meep('Histogram of relative risks in {0} register'.format(reg), 'Relative risk', 'Number of collocate pairs',
             'RR_{0}.png'.format(reg), [1 * i for i in range(18)], (0, 20))


def plot_verbtrends():
    target_pairs = ["('Prog1', 'Past')", "('PastPart→Noun', 'Acc')", "('Narr', 'Cop')"]
    pair_rows = []

    with open('../d5_statistics/cross_verb_trends.csv', 'r') as f:
        for r in csv.reader(f):
            if r[0] in target_pairs:
                pair_rows.append(r)
            elif r[0] == 'Pair':
                x_vals = r[1:-1]

    for p in pair_rows:
        for i in range(len(p)):
            if not p[i]:
                p[i] = None
            elif i != 0:
                p[i] = round(float(p[i]), 1)

        pyplot.plot(x_vals, p[1:-1])
        pyplot.axhline(y=p[-1], color='r', linestyle='-')
        meep('RR trend of {0}'.format(p[0]), 'Verb types', 'Relative risk', 'verb_trend_{0}.png'.format(p[0]),
             [e for e in x_vals if x_vals.index(e) % 20 == 0])


def plot_rrvsfreq():
    with open('../d5_statistics/assoc_stats/__assoc_stats.csv', 'r') as f:
        data = [(r[1], r[-1]) for r in csv.reader(f)][1:]

    pyplot.scatter([e[0] for e in data], [e[1] for e in data], s=5)
    # pyplot.yscale('log')
    meep('Relative risk by verb instance frequency', 'Relative risk', 'Number of verb instances', 'rrvsfreq.png',)


def plot_rr_vs_num_verbs():
    data = []

    with open('../d5_statistics/cross_verb_trends.csv', 'r') as f:
        first_row = True

        for r in csv.reader(f):
            if first_row:
                first_row = False
                continue

            num_verbs = len([c for c in r[1:-2] if c])
            data.append((float(r[-2]), int(num_verbs)))

    pyplot.scatter([e[0] for e in data], [e[1] for e in data], s=5)
    meep('Relative risk vs verb type frequency', 'Relative risk', 'Type frequency',
         'type_freq.png')

# plot_rr()
# plot_logrr()
# plot_rrci()
# plot_register()
# plot_verbtrends()
# plot_rrvsfreq()
plot_rr_vs_num_verbs()
exit(0)
