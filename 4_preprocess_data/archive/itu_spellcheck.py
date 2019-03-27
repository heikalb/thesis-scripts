"""
Send list of word windows to ITU for spellchecking
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import pipeline_caller
import csv


def main():
    caller = pipeline_caller.PipelineCaller()
    tool_name = "spellcheck"
    api_token = "sQj6zxcVt7JzWXHNTdRu3QRzc6i8KZz7"
    result = ''

    data = open('../1_data/query_results_all_joined_sents.csv')
    reader = csv.reader(data)
    sents = []
    indices =[]

    for r in reader:
        sents.append(r[0])
        indices.append(r[2])

    with open('../1_data/target_indices.txt', 'w') as f:
        f.write('\n'.join(indices))

    for i in range(0, 8):
        text = '\n'.join(sents[i*10000:(i+1)*10000])
        result += caller.call(tool_name, text, api_token)

    with open('../1_data/all_sents_spellchecked.txt', 'w') as f:
        f.write(result)


if __name__ == '__main__':
    main()
    exit(0)