# Formulaicity of Affixes in Turkish
This project contains scripts written for extracting and processing data on 
suffixes in the Turkish National Corpus for a Master's in Linguistics thesis.

## Motivation
The main idea of this project is formulaicity, which is the notion that some
sequences of multiple items (e.g., words) psycholinguistically function as 
units, despite their apparent decompositionality. This thesis project examines 
whether formulaicity also occurs among affixes, using the Turkish National 
Corpus (TNC) as a dataset. Although formulaicity is a psycholinguistic concept, 
this project looks for an evidence for it in distributional data in a corpus.

The main questions explored in this project are:

* Does affix formulaicity exist in the corpus?
* Is affix formulaicity a gradient or discrete phenomenon?
* Does formulaicity also apply to affixes and stems?

One contribution of this study is the method used to capture formulaicity 
between affixes. For this purpose, this study uses a measurement of association
called risk ratio, which is likely have never been used to measure collocation
in corpus studies. 


## Content and structure

The following are the directories in this repository, which sequentially 
correspond to the data collection, processing and analysis steps in this 
project:

* d0_prep_query_terms
  * Extract highest frequency verb stems from *A Frequency Dictionary of 
  Turkish*. 
* d1_get_data
  * Use the extracted verb stems to iteratively make queries on the TNC and
  download the corpus data file after each query.
* d2_data
  * Store corpus data files.
* d3_preprocess_data
  * Apply spell correction to corpus data, correct formatting errors in data 
  files and reduce data points to single sentences.
* d4_parse
  * Apply morphological parsing to words in the dataset. Reduce the data to
  the parses of target words.
* d5_statistics
  * Calculate risk ratio values for pairs of cooccurring suffixes in the 
  dataset. Values of other association measures were also calculated. Run 
  additional analyses on the risk ratio data.
* d6_graphics
  * Create graphs of corpus data and risk ratio data for the thesis document.

## Technology used
Programming languages used:
* Python 3.6
* Java

Python dependencies:
* selenium
* numpy
* scipy
* nltk
* matplotlib

The above packages can be installed with pip by entering, for example, 
`pip install nltk` in a command line.

Java dependency:
* [Zemberek-NLP](https://github.com/ahmetaa/zemberek-nlp)

This repository contains a JAR file of Zemberek-NLP (/zemberek-full.jar), which
may not be the current version. To get a possibly updated version of the JAR file
or for instructions on generating it yourself, refer to the README of 
Zemberek-NLP's repository (linked above). Once a Zemberek-NLP JAR file has been
installed or generated, it may need to be added to the build path of a project
containing /d4_parse/ParseMorphemes.java, which depends on Zemberek-NLP
for morphological parsing.

## Usage
### Using available data
The risk ratio dataset analyzed in the thesis are readily available in this 
repository. The data are in the following files, which also contain values of
other association measures:

* d5_statistics/association_stats/000__association_stats.csv
* d5_statistics/association_stats_spoken/000__association_stats_spoken.csv
* d5_statistics/association_stats_written/000__association_stats_written.csv
* d5_statistics/trigram/stem_trigram_rr.csv

These files can be downloaded and opened in a spreadsheet software.

### Generating data yourself
Most of the data files including ones containing query results, morphological
parses and association values by verbs are not available in this repository 
due to memory restriction. To generate data files yourself (including the ones
listed in the previous section) run the following programs in the following
order:

1. d0_prep_query_terms/get_freq_dict_verbs.py
2. d1_get_data/get_query_results.py
3. d3_preprocess_data/collect_queries.py
4. d4_parse/reduce_to_verbs.py
5. d4_parse/src/ParseMorphemes.java
6. d5_statistics/get_stats.py
7. d5_statistics/risk_ratio_analysis.py
8. d5_statistics/trigram/stem_trigram_assoc.py

Additional instructions:

* For running the Java file in step 5, you may need to add the 
JAR file for Zemberek-NLP to the build path first. The above programs can be run
from an integrated development environment (IDE) or the command line. 
* However, for the program in step 2, you have to run it in a command line to specify your username
and password of your TNC account (which you need to obtain beforehand). The 
minimum you need to enter is `python3 get_query_results.py -u exusername -p expassword`,
for example. You may tinker with d1_get_data/get_query_results.py so that you
can run it in an IDE with your user information.
* In step 2, when the program downloads data files, the data files will be saved
to the default download folder of the browser. You need to move those files to the directory
d2_data/query_results_freq_dict so that it could be used by programs in the next steps.
* In step 2, the program is currently designed to work only with Safari (the browser).

## Project status
This project is complete and is no longer in active development.

## Author
Heikal Badrulhisham <heikal93@gmail.com>

## License
MIT License 

Copyright © 2019 Heikal Badrulhisham 