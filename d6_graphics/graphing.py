import matplotlib.pyplot as pyplot
import csv
import math
import os


# General graphing function
def graph_it(title='', xlabel='', ylabel='', fname='',
             xticks=None, xlim=(), ylim=(), dim=(8, 6)):

    pyplot.gcf().set_size_inches(dim[0], dim[1])
    pyplot.grid(axis='y', alpha=0.5)
    pyplot.title(title, fontsize='x-large')
    pyplot.xlabel(xlabel, fontsize='medium')
    pyplot.ylabel(ylabel, fontsize='medium')

    if xlim:
        pyplot.xlim(xlim[0], xlim[1])

    if ylim:
        pyplot.ylim(ylim[0], ylim[1])

    if xticks:
        pyplot.xticks(xticks, rotation=90, fontsize='medium')

    pyplot.tight_layout()
    pyplot.savefig(fname)
    pyplot.close()


# Plot risk ratio values
def plot_rr():
    with open(main_data_file, 'r') as f:
        data = [r[1] for r in csv.reader(f)][1:]

    bin_edges = [0.5*i for i in range(36)]
    data = [round(float(e), 2) for e in data]
    pyplot.hist(data, bins=bin_edges, histtype='bar', edgecolor='w', alpha=0.8)

    graph_it('Distribution of risk ratio values',
             'Risk ratio (higher values not shown)',
             'Number of collocate pairs',
             'RR.png',
             [1*i for i in range(17)])


# Plot risk ratio confidence interval lower bounds
def plot_rrci():
    with open(main_data_file, 'r') as f:
        data = [r[8] for r in csv.reader(f)][1:]

    bin_edges = [0.5 * i for i in range(36)]
    data = [round(float(e), 2) for e in data]
    pyplot.hist(data, bins=bin_edges, histtype='bar', edgecolor='w', alpha=0.8)

    graph_it(
        'Distribution of risk ratio values (confidence interval lower bounds)',
        'Risk ratio confidence interval lower bounds (higher values not shown)',
        'Number of collocate pairs',
        'RR_ci.png',
        [1*i for i in range(17)])


# Plot log risk ratios
def plot_logrr():
    with open(main_data_file, 'r') as f:
        data = [r[1] for r in csv.reader(f)][1:]

    data = [round(math.log(float(e)), 2) for e in data]
    pyplot.hist(data, bins=[i*0.5 for i in range(-16, 24)], histtype='bar',
                edgecolor='w', alpha=0.8)

    graph_it('Distribution of log risk ratio',
             'Log risk ratio',
             'Number of collocate pairs',
             'RR_log.png',
             [i for i in range(-8, 12)])


def plot_register():
    for reg in ['spoken', 'written']:
        file_path = '../d5_statistics/association_stats_{0}/\
                     000__association_stats_{0}.csv'

        with open(file_path.format(reg), 'r') as f:
            data = [r[1] for r in csv.reader(f)][1:]

        bin_edges = [0.5*i for i in range(36)]
        data = [round(float(e), 2) for e in data]
        pyplot.hist(data, bin_edges, histtype='bar', edgecolor='w', alpha=0.8)

        graph_it('Histogram of risk ratios in {0} register'.format(reg),
                 'Risk ratio (higher values not shown)',
                 'Number of collocate pairs',
                 'RR_{0}.png'.format(reg),
                 [1 * i for i in range(18)],
                 (0, 20))


def plot_verbtrends():
    target_pairs = ["('Prog1', 'Past')", "('PastPart→Noun', 'Acc')",
                    "('Narr', 'Cop')"]
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

        graph_it('RR trend of {0}'.format(p[0]),
                 'Verb types',
                 'Risk ratio',
                 'verb_trend_{0}.png'.format(p[0]),
                 [e for e in x_vals if x_vals.index(e) % 20 == 0])


def plot_rrvsfreq():
    with open(main_data_file, 'r') as f:
        data = [(r[1], r[-1]) for r in csv.reader(f)][1:]

    pyplot.scatter([e[0] for e in data], [e[1] for e in data], s=5)

    graph_it('Risk ratio by verb instance frequency',
             'Risk ratio',
             'Number of verb instances',
             'rrvsfreq.png',)


def plot_rr_vs_num_verbs():
    data = []

    with open('../d5_statistics/cross_verb_trends.csv', 'r') as f:
        first_row = True

        for r in csv.reader(f):
            if first_row:
                first_row = False
                continue

            num_verbs = len([c for c in r[1:-2] if c])
            data.append((r[-2], num_verbs))

    pyplot.scatter([e[0] for e in data], [e[1] for e in data], s=5)

    graph_it('Risk ratio vs verb type frequency',
             'Risk ratio',
             'Type frequency',
             'type_freq.png')


def plot_num_datapoints():
    filenames = os.listdir('../d2_data/query_results_freq_dict/')
    filenames.sort()
    nums_data = []
    stems = []

    for filename in filenames:
        file_path = '../d2_data/query_results_freq_dict/'

        with open(os.path.join(file_path, filename), 'r') as f:
            num_data = len([r for r in csv.reader(f)][1:])
            nums_data.append(num_data)

        stem = filename.split('_')[2]
        stems.append(stem)

    print(len(nums_data))
    print(sum(nums_data))
    exit()

    pyplot.bar(stems, nums_data)

    graph_it('Distribution of datapoints by verb types',
             'Verb types',
             'Number of datapoints',
             'num_datapoints.png',
             xticks=[s for s in stems if stems.index(s) % 20 == 0])


def plot_integrity():
    with open(main_data_file, 'r') as f:
        data = [r for r in csv.reader(f)][1:]

    data = [float(r[-2]) / float(r[-3]) for r in data]
    pyplot.hist(data, bins=[i * 0.1 for i in range(0, 11)],
                histtype='bar', edgecolor='w', alpha=0.8)

    graph_it('Distribution of collocate pair integrity',
             'Integrity',
             'Number of collocate pairs',
             'trigram_integrity.png',
             [i*0.1 for i in range(0, 11)])


def plot_stem_trigram_rr():
    with open('../d5_statistics/trigram/stem_trigram_rr.csv', 'r') as f:
        data = [r[2] for r in csv.reader(f)][1:]

    bin_edges = [0.5*i for i in range(21)]
    data = [round(float(e), 2) for e in data]
    pyplot.hist(data, bins=bin_edges, histtype='bar', edgecolor='w', alpha=0.8)

    graph_it('Distribution of risk ratio of stem-trigram pairs',
             'Risk ratio (higher values not shown)',
             'Number of collocate pairs',
             'stem_trigram_rr.png',
             [1*i for i in range(11)])


if __name__ == '__main__':
    main_data_file = '../d5_statistics/association_stats/\
                      000__association_stats.csv'

    # plot_rr()
    plot_rrci()
    # plot_logrr()
    # plot_register()
    # plot_verbtrends()
    # plot_rrvsfreq()
    # plot_rr_vs_num_verbs()
    # plot_num_datapoints()
    # plot_integrity()
    # plot_stem_trigram_rr()
    exit(0)
