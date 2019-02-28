# -*- coding: utf-8 -*-
"""
Filter out results from the file for 'anla-' to only include 'anlat-' (the base verb plus the causative)
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import csv

saved_lines = []

with open('../data/query_results/tnc_query_result_13_attn.csv', 'rb') as f:
    rdr = csv.reader(f)

    for row in rdr:
        if 'anlat' in row[3].lower():
            saved_lines.append(row)

with open('../data/query_results/tnc_query_result_13.csv', 'wb') as f:
    wrtr = csv.writer(f)

    for line in saved_lines:
        wrtr.writerow(line)