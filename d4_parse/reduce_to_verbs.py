"""
Reduce the file of parses to parses of target verbs only, and separately
save parsing errors.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
import os
from collections import Counter


def get_indices(file_path):
    """
    Get position of target verbs in the context windows in a data file.
    :param file_path: path of data file
    :return: list of indices of target verbs
    """

    with open(file_path) as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [int(row[2]) for row in reader]

    return indices


def get_register(file_path):
    """
    Get register of data points in a data file.
    :param file_path: path of data file
    :return: list of registers for data points ('w' or 'r')
    """
    with open(file_path) as f:
        reader = csv.reader(f, delimiter='\t')
        indices = [row[-1] for row in reader]

    return indices


def get_parses(parse_file_names, parse_dir):
    """
    Get verb parses and parsing errors.
    :param parse_file_names: list of filenames of parse files
    :param parse_dir: the directory of parse files
    :return: a list of verb parses and a list of parsing errors
    """
    verb_parses = []
    parse_errors = []

    # Process each parse file
    for file_name in parse_file_names:
        file_path = os.path.join(parse_dir, file_name)
        parses = open(file_path, 'r').read().split('\n')

        # Get indices of target verbs
        fnum, stem = file_name.split('_')[:-1]
        indices = get_indices(f'../d2_data/joined/{fnum}_{stem}_joined.tsv')
        registers = get_register(f'../d2_data/joined/{fnum}_{stem}_joined.tsv')

        # Get target verbs and parses with errors
        for i in range(len(indices)):
            cur_parses = [p for p in parses[i][1:-1].split(', ')
                          if ':Punc' not in p]

            # Divide data into verb parses and parsing errors
            if 'UNK' not in cur_parses[indices[i]]:
                new_line = f'{cur_parses[indices[i]]} {registers[i]} {stem}'
                verb_parses.append(new_line)
            else:
                parse_errors.append(cur_parses[indices[i]])

    return verb_parses, parse_errors


def save_data(verb_parses, parse_errors):
    """
    Save verb parses and parsing errors in .txt files.
    :param verb_parses: list of verb parses
    :param parse_errors: list of parsing errors
    """
    with open('verb_parses.txt', 'w') as f:
        f.write('\n'.join(verb_parses))

    parse_error_counter = Counter(parse_errors)
    parse_errors = sorted(list(set(parse_errors)),
                          key=lambda x: parse_error_counter[x], reverse=True)

    with open('parse_errors.txt', 'w') as f:
        lines = [f'{k} {parse_error_counter[k]}' for k in parse_errors]
        f.write('\n'.join(lines))


def main():
    """
    Main method.
    """
    # Get individual verb parse files
    parse_dir = 'parses/'
    parse_files = os.listdir(parse_dir)
    parse_file_names = [f for f in parse_files if 'parses.txt' in f]
    parse_file_names.sort()

    # Get verb parses and parsing errors
    verb_parses, parse_errors = get_parses(parse_file_names, parse_dir)

    # Save data and parse errors
    save_data(verb_parses, parse_errors)

    # Display summary statistics
    print('Number of verb parses: ', len(verb_parses))
    print('Number of parse errors: ', len(parse_errors))
    print('Net verb parses: ', len(parse_errors) - len(parse_errors))


if __name__ == '__main__':
    main()
    exit(0)
