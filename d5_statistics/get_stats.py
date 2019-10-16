"""
Get association data from morphological parses of verbs extracted from the TNC.
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import colloc_measures as cm
from collections import defaultdict
import re
import os
import csv


def tally(freq, stem, register=''):
    """
    Tally frequencies of suffixes and collocate pairs in the dataset.
    :param freq: various types of frequency data
    :param stem: verb stem (if given to narrow down data)
    :param register: register of the subcorpus (if given to narrow down data)
    """
    for parse in parses:
        parse = parse.split()

        # Stem that appears in the morphological parse
        stem_in_parse = parse[1].split(':')[0]
        # Stem that is determined for the word prior to parsing
        stem_end_parse = parse[3]

        # Skip parses for a different stem or wrong parses
        if (stem and stem_in_parse not in stem) or \
           (pos not in parse[0] and pos not in parse[1]) or \
           (register and register != parse[2]):
            continue

        # Get suffixes, exclude stems. Collapse allomorphs.
        # Remove unneeded suffixes the parser introduced
        suffixes = re.split(suffix_boundary, parse[1])[1:]
        suffixes = remove_forbidden_suffixes(suffixes)
        suffixes = [re.sub(morph_boundary, '', s) for s in suffixes]

        # Update frequencies
        update_freq(freq, suffixes, stem_end_parse)

    # Report frequencies
    print(f'Stem: {stem}\tPair types: {len(freq["pair"])}\t'
          f'Pair instances: {sum([freq["pair"][p] for p in freq["pair"]])}')


def update_freq(freq, suffixes, stem_end_parse):
    """
    For a given morphologically parsed word, update frequencies based on each
    morpheme within.
    :param freq: various types of frequency data
    :param suffixes: list of suffixes in a morphological parse
    :param stem_end_parse: stem of the current parse
    """
    for i in range(len(suffixes)):
        # Update single suffix frequency
        freq['suffix'][suffixes[i]] += 1

        # Update suffix pair cooccurrence frequency
        for j in range(i + 1, len(suffixes)):
            curr_pair = (suffixes[i], suffixes[j])
            freq['pair'][curr_pair] += 1

            # Update frequency of the two suffixes being adjacent
            if j - i == 1:
                freq['adjacency'][curr_pair] += 1

            # Update verb stem-wise frequency of pairs
            if stem_end_parse not in freq['stem'][curr_pair]:
                freq['stem'][curr_pair].append(stem_end_parse)
    

def remove_forbidden_suffixes(suffixes):
    """
    For a given sequence of suffixes, remove the following:
    -word final 3rd person singular
    Helper method for tally()
    :param suffixes: list of suffixes
    :return: list of suffixes with unneeded suffixes removed
    """
    if suffixes[-1] == 'A3sg':
        return [suff for suff in suffixes if ':' in suff] + [suffixes[-1]]
    else:
        return [suff for suff in suffixes if ':' in suff]


def get_association(freq, measure_vals, ci_dict):
    """
    Calculate association measurement values for collocate pairs.
    :param freq: various types of frequency data
    :param measure_vals: values of association measurements
    :param ci_dict: confidence intervals on association values
    """
    num_suffixes = sum(freq['suffix'][s] for s in freq['suffix'])

    for pair in freq['pair']:
        suff_1, suff_2 = pair

        for msr in measures:
            args = [freq['suffix'][suff_1], freq['suffix'][suff_2],
                    freq['pair'][pair], num_suffixes,
                    suff_1, suff_2, freq['pair']]

            stat = measures[msr](*args)

            if type(stat) == tuple:
                measure_vals[msr][pair] = stat[0]
                ci_dict[msr][pair] = stat[1]
            else:
                measure_vals[msr][pair] = stat


def save_data(freq, file_affix, dir_affix, stem, measure_vals, ci_dict):
    """
    Save association values in .csv files.
    :param freq: various types of frequency data
    :param file_affix: affix on data file to save (index)
    :param dir_affix: affix on directory of data file (register)
    :param stem: verb stem of the current subdataset (if given)
    :param measure_vals: values of association measurements
    :param ci_dict: onfidence intervals on association values
    """

    # Create file if it's not alreeady there
    if not os.path.isdir(f'association_stats{dir_affix}'):
        os.mkdir(f'association_stats{dir_affix}')

    # Fill up data
    file_path = f'association_stats{dir_affix}/{file_affix}_{stem}' +\
                f'_association_stats{dir_affix}.csv'

    with open(file_path, 'w') as f:
        csv_writer = csv.writer(f)

        # Column labels
        first_row = ["collocate_pair",
                     *[m for m in measure_vals],
                     *[f'{k}_confidence_interval_{d}'
                       for k in confidence_intervals
                       for d in ['left', 'right']],
                     'suffix1_frequency', 'suffix2_frequency',
                     'suffix1-suffix2_frequency',
                     'suffix1-suffix2_adjacent_frequency', 'stem_freq']

        csv_writer.writerow(first_row)

        # Fill in row values, sort by risk ratio
        sorted_pairs = sorted(freq['pair'], reverse=True,
                              key=lambda x: measure_vals['risk_ratio'][x])

        for k in sorted_pairs:
            row = [k,
                   *[measure_vals[m][k] for m in measure_vals],
                   *[ci_dict[c][k][i] for c in ci_dict for i in [0, 1]],
                   *[freq['suffix'][suff] for suff in k],
                   freq['pair'][k], freq['adjacency'][k], len(freq['stem'][k])]

            csv_writer.writerow(row)


def main(stem="", file_affix="", dir_affix='', register=''):
    """
    Get frequencies of suffixes and collocate pairs and other frequency data
    from morphological parses and filter out data based on stem and register (if
    specified).
    Then calculate association values on each collocate pair.
    Then save association values and other frequency data in .csv files.
    :param stem: stem for filtering the data (empty string for no filter)
    :param file_affix: affix on data file to be saved (index)
    :param dir_affix: affix on directory of data file (register)
    :param register: register for filtering the data(empty string for no filter)
    """
    # Dictionaries for association values and confidence intervals
    measure_vals = dict(zip(measures, [dict() for m in measures]))
    ci_dict = dict(zip(confidence_intervals,
                       [dict() for m in confidence_intervals]))
    
    # Various types of frequency data to collect
    freq = {'suffix': defaultdict(int), 'pair': defaultdict(int),
            'adjacency': defaultdict(int), 'stem': defaultdict(list)}

    # Tally suffixes and suffix collocates
    tally(freq, stem, register)

    # Get association measures
    get_association(freq, measure_vals, ci_dict)

    # Save stats in files
    save_data(freq, file_affix, dir_affix, stem, measure_vals, ci_dict)


if __name__ == "__main__":
    # Run main operations in main() interatively here by verb stem and register

    # Association measurements and measurement confidence intervals
    measures = {'risk_ratio': cm.risk_ratio,
                'risk_ratio_reverse':  cm.risk_ratio_reverse,
                'odds_ratio': cm.odds_ratio,
                'mutual_information': cm.mutual_info,
                'dice_coefficient': cm.dice_coeff,
                't_score': cm.t_score,
                'chi_squared': cm.chi_sq}
    
    # Association measurements with confidence intervals
    confidence_intervals = ['risk_ratio', 'risk_ratio_reverse']
    
    # Information for segmenting parse data
    pos = 'Verb'
    suffix_boundary = r'[\|\+]'
    morph_boundary = r'.*:'

    # Get parses
    with open('../d4_parse/verb_parses.txt', 'r') as f:
        parses = f.read().split('\n')
    
    # Get verb stems and indices. Use empty string for selecting all verb stems
    verb_stem_file = open('../d0_prep_query_terms/freq_dict_verbs.txt', 'r')
    stems = [""] + verb_stem_file.read().split('\n')
    i = 0

    # Get statistics for each verb type
    for stem in stems:
        main(stem, f'00{i}'[-3:])
        # colloc_stats(stem, f'00{i}'[-3:], dir_affix='_written', register='w')
        # colloc_stats(stem, f'00{i}'[-3:], dir_affix='_spoken', register='s')
        i += 1

    exit(0)
