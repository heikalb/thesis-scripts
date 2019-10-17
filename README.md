# Formulaicity of Affixes in Turkish
This project contains scripts written for extracting and processing data on 
suffixes in the Turkish National Corpus for a Master's in Linguistics thesis.

## Motivation
The main idea of this project is formulaicity, which is the notion that some
sequences of multiple items (e.g., words) psycholinguistically function as 
units, despite their apparent decompositionality. This thesis project examines 
whether formulaicity also occurs among affixes, using the Turkish National 
Corpus (TNC) as a dataset. Although formulaicity is a psycholinguistic concept, 
this project looks for an evidence for it through the distribution of affixes in 
a corpus.

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
### Generating data yourself

##Project status
This project is no longer in active development.


##Author
Heikal Badrulhisham <heikal93@gmail.com>

## License
MIT License 

Copyright (c) 2019 Heikal Badrulhisham 