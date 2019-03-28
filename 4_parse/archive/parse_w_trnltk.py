# -*- coding: utf-8 -*-
"""
Parse verbs (only) using TRNLTK
Note: because of the state of TRNLTK in python, this script has to be run in Python 2
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv
from trnltk.playground import playground as pg


# Morphological parser — a modified copy of the one in TRNLTK. Printing is disabled, and the function
# now returns the parsing. 
def morph_parse(word_str, *syntactic_categories):
    word_str = word_str.decode(encoding='UTF—8')
    parse_results = pg.contextless_parser.parse(word_str)

    if syntactic_categories:
        parse_results = filter(lambda parse_result: parse_result.get_last_state().syntactic_category in syntactic_categories, parse_results)
    
    parses = []

    if parse_results:
        for parse_result in parse_results:
            formatted_output = pg.formatter.format_morpheme_container_for_tests(parse_result)
            parses.append(formatted_output.encode('utf-8'))
                        
    return parses


def get_shortest_parse(parse_list):
    length_parse = [(len(p.split('_')), p) for p in parse_list]
    return min(length_parse)[1]


def main():
    # Get list of verbs
    verb_file = open('../2_data/all_verbs_spellchecked.txt', 'rb')
    words = verb_file.read().split('\n')

    # Morphlogical parses and numbers to track parser performance
    parses = []
    one_parse_found = 0
    mult_parse_found = 0
    no_parse_found = 0
    
    # Get parses
    for w in words:
        curr_parses = morph_parse(w)
        curr_parses = [cp for cp in curr_parses if cp.split('_')[1] == 'Verb']
        parse_status = ''
        parse = ''

        # Get 3_parse information
        if len(curr_parses) == 1:
            one_parse_found += 1
            parse_status = 'parsed_single'
            parse = curr_parses[0]
        elif len(curr_parses) > 1:
            mult_parse_found += 1
            parse_status = 'parsed_multiple'
            parse = get_shortest_parse(curr_parses)
        else:
            no_parse_found += 1
            parse_status = 'parse_not_found'
            parse = '<no_parse>'

        parses.append([w, parse, parse_status])

    # Display findings about parser performance
    print('One 3_parse found: ', one_parse_found)
    print('Multiple parses found: ', mult_parse_found)
    print('No 3_parse found: ', no_parse_found)

    with open('morph_parses.csv', 'wb') as f:
        csv_writer = csv.writer(f)

        for p in parses:
            csv_writer.writerow(p)

    verb_file.close()


if __name__ == "__main__":
    main()
    exit(0)
