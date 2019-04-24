import matplotlib.pyplot as pyplot
import csv

with open('../d5_statistics/assoc_stats/__assoc_stats.csv', 'r') as f:
    data = [r[1] for r in csv.reader(f)][1:]

bin_edges = [0.5*i for i in range(36)]
data = [round(float(e), 2) for e in data]
n, bins, patches = pyplot.hist(data, bins=bin_edges, histtype='bar', edgecolor='w', alpha=0.8)

pyplot.gcf().set_size_inches(12, 9)
pyplot.title('Histogram of relative risks')
pyplot.xlabel('Relative risk')
pyplot.ylabel('Number of collocate pairs')
pyplot.xlim(0, 20)
pyplot.xticks([1*i for i in range(18)])
pyplot.savefig('RR.png')
exit(0)