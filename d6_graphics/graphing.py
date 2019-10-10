"""
Create figures on specific subsets of the data.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""

import matplotlib.pyplot as pyplot
import csv
import math
import os


def graph_it(title='', xlabel='', ylabel='', fname='', xticks=None, xlim=(),
             ylim=(), dim=(6, 4)):
    """
    Create figures based on given parameters.
    :param title: title of the figure
    :param xlabel: label for the x-axis
    :param ylabel: label for the y-axis
    :param fname: name of the image file to be saved
    :param xticks: x-values that will be labeled in the graph
    :param xlim: interval of x-values to be displayed
    :param ylim: interval of y-values to be displayed
    :param dim: dimension of the image
    """

    # Set mandatory graph parameters
    pyplot.gcf().set_size_inches(dim)
    pyplot.grid(axis='y', alpha=0.5)
    font = {'fontname': 'Cormorant'}
    # pyplot.title(title, fontsize='11', ** font)
    pyplot.xlabel(xlabel, fontsize='11', ** font)
    pyplot.ylabel(ylabel, fontsize='11', ** font)
    pyplot.yticks(fontsize='11', ** font)

    # Set optional graph parameters
    if xlim:
        pyplot.xlim(xlim[0], xlim[1])
    if ylim:
        pyplot.ylim(ylim[0], ylim[1])
    if xticks:
        pyplot.xticks(xticks, rotation=90, fontsize='11', ** font)

    # Final processing
    pyplot.tight_layout()
    pyplot.savefig(fname, dpi=300)
    pyplot.close()


def plot_num_datapoints():
    """
    Plot number of datapoints by verb types for Figure 3.
    """
    # Get query result files of verbs, sorted by frequency ranking
    data_dir = '../d2_data/query_results_freq_dict/'
    filenames = os.listdir(data_dir)
    filenames.sort()

    # x- and y-axis labels
    stems = []
    nums_data = []

    # Get number of datapoint per verb
    for filename in filenames:
        # Get frequency
        with open(os.path.join(data_dir, filename), 'r') as f:
            num_data = len([r for r in csv.reader(f)][1:])
            nums_data.append(num_data)

        # Get stem from file name
        stem = filename.split('_')[2]
        stems.append(stem)

    # Create graph
    title = 'Distribution of datapoints by verb types'
    xlabel = 'Verb types'
    ylabel = 'Number of datapoints'
    fname = 'num_datapoints.png'
    xticks = [s for s in stems if stems.index(s) % 30 == 0]

    pyplot.bar(stems, nums_data)
    graph_it(title, xlabel, ylabel, fname, xticks)


def plot_rr():
    """
    Plot risk ratio values for Figure 5 (1).
    """
    # Get risk ratios from main dataset
    risk_ratios = [round(float(r[1]), 2) for r in all_data]

    # Create graph
    title = 'Distribution of risk ratio values'
    xlabel = 'Risk ratio (higher values not shown)'
    ylabel = 'Number of collocate pairs'
    fname = 'RR.png'
    xticks = [1*i for i in range(17)]
    bin_edges = [0.5*i for i in range(36)]

    pyplot.hist(risk_ratios, bin_edges, histtype='bar', edgecolor='w', alpha=.8)
    graph_it(title, xlabel, ylabel, fname, xticks)


def plot_rrci():
    """
    Plot risk ratio confidence interval lower bounds for Figure 5 (2).
    """
    # Get risk ratio lower bounds from main dataset
    rr_ci = [round(float(r[8]), 2) for r in all_data]

    # Create graph
    title = 'Distribution of risk ratios (confidence interval lower bounds)'
    xlabel = 'Risk ratio confidence interval lower bounds ' \
             '(higher values not shown)'
    ylabel = 'Number of collocate pairs'
    fname = 'RR_ci.png'
    xticks = [1*i for i in range(17)]
    bin_edges = [0.5 * i for i in range(36)]

    pyplot.hist(rr_ci, bin_edges, histtype='bar', edgecolor='w', alpha=0.8)
    graph_it(title, xlabel, ylabel, fname, xticks)


def plot_logrr():
    """
    Plot log risk ratios for Figure 6.
    """
    # Get log risk ratio from main dataset
    log_rr = [round(math.log(float(r[1])), 2) for r in all_data]

    # Create graph
    title = 'Distribution of log risk ratio'
    xlabel = 'Log risk ratio'
    ylabel = 'Number of collocate pairs'
    fname = 'RR_log.png'
    xticks = [i for i in range(-8, 12)]
    bin_edges = [i*0.5 for i in range(-16, 24)]

    pyplot.hist(log_rr, bin_edges, histtype='bar', edgecolor='w', alpha=.8)
    graph_it(title, xlabel, ylabel, fname, xticks)


def plot_integrity():
    """
    Plot integrity ratios for Figure 7.
    """
    # Get integrity ratios from main datset
    integrity = [float(r[-2])/float(r[-3]) for r in all_data if float(r[1]) > 1]

    # Create graph
    title = 'Distribution of collocate pair integrity'
    xlabel = 'Integrity'
    ylabel = 'Number of collocate pairs'
    fname = 'trigram_integrity.png'
    xticks = [i*0.1 for i in range(0, 11)]
    bin_edges = [i * 0.1 for i in range(0, 11)]

    pyplot.hist(integrity, bin_edges, histtype='bar', edgecolor='w', alpha=.8)
    graph_it(title, xlabel, ylabel, fname, xticks)


def plot_stem_trigram_rr():
    """
    Plot risk ratios of stem-trigram pairs for Figure 8.
    """
    # Get risk ratio of stem-trigrams
    with open('../d5_statistics/trigram/stem_trigram_rr.csv', 'r') as f:
        risk_ratios = [r[2] for r in csv.reader(f)][1:]
        risk_ratios = [round(float(e), 2) for e in risk_ratios]

    # Create graph
    title = 'Distribution of risk ratio of stem-trigram pairs'
    xlabel = 'Risk ratio (higher values not shown)'
    ylabel = 'Number of collocate pairs'
    fname = 'stem_trigram_rr.png'
    xticks = [1*i for i in range(11)]
    bin_edges = [0.5*i for i in range(21)]

    pyplot.hist(risk_ratios, bin_edges, histtype='bar', edgecolor='w', alpha=.8)
    graph_it(title, xlabel, ylabel, fname, xticks)


if __name__ == '__main__':
    # Get main dataset
    data_file = '../d5_statistics/association_stats/000__association_stats.csv'

    with open(data_file, 'r') as f:
        all_data = [r for r in csv.reader(f)][1:]
        all_data = [r for r in all_data
                    if float(r[12]) >= 100 and float(r[13]) >= 100]

    # Plot specific data
    # plot_num_datapoints()
    # plot_rr()
    # plot_rrci()
    # plot_logrr()
    plot_integrity()
    # plot_stem_trigram_rr()

    exit(0)
