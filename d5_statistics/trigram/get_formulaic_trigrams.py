"""
Find trigrams in which both constituent bigrams are associated.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
from nltk import ngrams


def main():
    """
    Get trigrams where both constituent bigrams are associated, and save
    the data.
    """
    # Get suffix trigrams
    with open('suffix_trigrams.txt', 'r') as f:
        trigram_lines = f.read().split('\n')

    # Get risk ratio of suffix pairs
    with open('../association_stats/000__association_stats.csv', 'r') as f:
        data = [r for r in csv.reader(f)][1:]
        pair_risk_ratios = dict(zip([r[0] for r in data],
                                    [float(r[1]) for r in data]))

    # Get risk ratios of stem-trigrams
    saved_trigrams = filter_trigrams(trigram_lines, pair_risk_ratios)

    # Save trigram data, sorted by trigram frequency
    saved_trigrams.sort(reverse=True, key=lambda x: x[-2])

    with open('formulaic_trigrams.csv', 'w') as f:
        csv.writer(f).writerows(saved_trigrams)


def filter_trigrams(trigram_lines, pair_risk_ratios):
    """
    Go through list of trigrams and filter ones where both constituent trigrams
    are associated.
    :param trigram_lines: lines of trigrams and their frequencies
    :param pair_risk_ratios: risk ratios of suffix pairs
    :return: trigrams where both constituent trigrams are associated.
    """
    saved_trigrams = []

    for trigram_line in trigram_lines:
        # Get information from trigram file line
        trigram, trigram_freq = trigram_line.split(') ')
        trigram_freq = int(trigram_freq)

        # Form tuples from trigram strings
        trigram = trigram[1:].split(', ')
        trigram = tuple([suffix[1:-1] for suffix in trigram])

        # Get constituent bigrams within the trigram
        bigrams = [bigram for bigram in ngrams(list(trigram), 2)]

        try:
            # Get risk ratio of each bigram
            curr_rr = [pair_risk_ratios[str(bigram)] for bigram in bigrams]

            # Save trigrams where the constituent trigams are associated
            if all([rr > 1 for rr in curr_rr]):
                new_line = [*list(trigram), curr_rr, trigram_freq,
                            min(curr_rr[0]/curr_rr[1], curr_rr[1]/curr_rr[0])]

                saved_trigrams.append(new_line)
        except KeyError:
            continue

        return saved_trigrams


if __name__ == '__main__':
    main()
    exit(0)
