"""
Reduce the file of parses to parses of target verbs only.
"""
import csv


# Get position of target verbs in the context windows
def get_verb_indices():
    with open('../data/query_results_all_joined_sents_.tsv') as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [int(row[2]) for row in reader]

    return indices


def main():
    verb_parses = []
    parses = open('parses.txt', 'r').read().split('\n')
    indices = get_verb_indices()

    for i in range(len(indices)):
        curr_word_parses = [p for p in parses[i][1:-1].split(', ') if ':Punc' not in p]
        verb_parses.append(curr_word_parses[indices[i]])

    with open('verb_parses.txt', 'w') as f:
        f.write('\n'.join(verb_parses))


if __name__ == '__main__':
    main()
    exit(0)