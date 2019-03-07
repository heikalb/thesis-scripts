import csv
from collections import defaultdict
import re
import colloc_measures as cm


def main():
    # Open file of parses
    parse_file = open('../parse/morph_parses.csv')
    csv_reader = csv.reader(parse_file)

    # Stats
    suffix_counts = defaultdict(int)
    cooccurence_counts = defaultdict(int)
    num_suffixes = 0
    mutual_infos = {}
    t_scores = {}
    dice_coeff = {}
    chi_squared = {}

    # Go through parses
    for row in csv_reader:
        # Skip unparseable words
        if row[2] == 'parse_not_found':
            continue

        # Only consider non-null morphemes
        parse = row[1]
        suffixes = [s for s in parse.split('_') if '[' in s or ']' in s]

        # Put back 3.Sg null morphemes
        if parse[-4:] == 'A3sg':
            suffixes.append('A3sg')

        # Collapse allomorphs
        suffixes = [re.sub(r'\(.*\)', '', s) for s in suffixes]

        # Count suffix co-occurrences
        num_suffixes += len(suffixes)
        for i in range(len(suffixes)):
            # Updata single suffix count
            suffix_counts[suffixes[i]] += 1

            # Update count for co-occurring pair
            for j in range(i + 1, len(suffixes)):
                curr_key = '{0} & {1}'.format(suffixes[i], suffixes[j])
                cooccurence_counts[curr_key] += 1

    # Get association measures
    for k in cooccurence_counts:
        morpheme_pair = k.split(' & ')
        morph_1, morph_2 = morpheme_pair[0], morpheme_pair[1]

        mutual_infos[k] = (cm.mutual_info(cooccurence_counts, suffix_counts, k, morph_1, morph_2, num_suffixes),
                           suffix_counts[morph_1], suffix_counts[morph_2])

        t_scores[k] = (cm.t_score(cooccurence_counts, suffix_counts, k, morph_1, morph_2, num_suffixes),
                              suffix_counts[morph_1], suffix_counts[morph_2])

        dice_coeff[k] = (cm.dice_coeff(cooccurence_counts, suffix_counts, k, morph_1, morph_2),
                     suffix_counts[morph_1], suffix_counts[morph_2])

        chi_squared[k] = (cm.chi_squared(cooccurence_counts, suffix_counts, k, morph_1, morph_2, num_suffixes),
                       suffix_counts[morph_1], suffix_counts[morph_2])

    # Save data
    with open('cooccurrence_count.csv', 'w') as f:
        csv_writer = csv.writer(f)

        for k in cooccurence_counts:
            csv_writer.writerow([k, cooccurence_counts[k]])

    with open('suffix_count.csv', 'w') as f:
        csv_writer = csv.writer(f)

        for k in suffix_counts:
            csv_writer.writerow([k, suffix_counts[k]])

    with open('mutual_info.csv', 'w') as f:
        csv_writer = csv.writer(f)

        for k in mutual_infos:
            csv_writer.writerow([k, mutual_infos[k][0], mutual_infos[k][1], mutual_infos[k][2]])

    with open('t_scores.csv', 'w') as f:
        csv_writer = csv.writer(f)

        for k in t_scores:
            csv_writer.writerow([k, t_scores[k][0], t_scores[k][1], t_scores[k][2]])

    with open('dice_coeff.csv', 'w') as f:
        csv_writer = csv.writer(f)

        for k in dice_coeff:
            csv_writer.writerow([k, dice_coeff[k][0], dice_coeff[k][1], dice_coeff[k][2]])

    with open('chi_squared.csv', 'w') as f:
        csv_writer = csv.writer(f)

        for k in chi_squared:
            csv_writer.writerow([k, chi_squared[k][0], chi_squared[k][1], chi_squared[k][2]])


if __name__ == "__main__":
    main()
    exit(0)
