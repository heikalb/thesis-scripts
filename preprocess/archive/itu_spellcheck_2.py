"""
Send list of word windows to ITU for spellchecking
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import pipeline_caller
import csv
from collections import defaultdict
import pickle
import os

# For calling ITU pipeline
caller = pipeline_caller.PipelineCaller()
tool_name = "spellcheck"
api_token = "sQj6zxcVt7JzWXHNTdRu3QRzc6i8KZz7"

# Dictionary of past spellcheck results
if os.path.isfile('spellcheck_history.pkl'):
    spellcheck_history = pickle.load(open('spellcheck_history.pkl', 'rb'))
else:
    spellcheck_history = defaultdict(str)


def spellcheck(word):
    if word in spellcheck_history:
        return spellcheck_history[word]
    else:
        sc = caller.call(tool_name, word, api_token).replace('\r\n', '')
        spellcheck_history[word] = sc
        return sc


def main():
    # Gather data from csv
    results = []
    data = open('../data/query_results_all_joined_sents.csv')
    reader = csv.reader(data)
    sents = []
    indices = []

    for r in reader:
        sents.append(r[0])
        indices.append(r[2])

    # Save indices of target verbs
    with open('../data/target_indices.txt', 'w') as f:
        f.write('\n'.join(indices))

    # Send contexts to ITU for spellchecking
    i = 0
    start = 0
    for s in sents[start:]:
        try:
            spellchecked_words = [spellcheck(w) for w in s.split()]
            results.append(' '.join(spellchecked_words))
            i += 1
        except ConnectionResetError:
            True

        if i % 5000 == 0 or i == len(sents[start:]):
            with open('../data/all_sents_spellchecked{0}.txt'.format(i), 'w') as f:
                f.write('\n'.join(results))

            pickle.dump(spellcheck_history, open("spellcheck_history.pkl", 'wb'))


if __name__ == '__main__':
    main()
    exit(0)
