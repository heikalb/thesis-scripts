"""
Make lemma-based queries on the TNC web interface based on a list of lemmas
Heikal Badrulhisham <heikal93@gmail.com>, 2019
"""
import argparse
from selenium import webdriver
from selenium.common.exceptions import *
import time
from selenium.webdriver.support.ui import Select


def sign_in():
    """
    Sign into a TNC account
    """
    while True:
        try:
            browser.find_element_by_css_selector(
                'input[placeholder=Email]').send_keys(email)

            browser.find_element_by_name('password').send_keys(password)
            browser.find_element_by_css_selector('input[type=submit]').click()
            break
        except NoSuchElementException:
            time.sleep(1)

    while browser.find_elements_by_name('password'):
        time.sleep(1)


def open_query():
    """
    Open the page containing lemma-based query function on the TNC
    """
    while True:
        try:
            browser.find_elements_by_css_selector(
                '.btn-group.col-md-12 .btn.btn-default')[1].click()
            break
        except Exception:
            time.sleep(1)


def submit_query(search_term):
    """
    Submit query on the TNC
    :param search_term: term to query on
    """
    while True:
        try:
            browser.find_element_by_id('query').send_keys(search_term)
            pos_options = Select(browser.find_element_by_id('type'))
            pos_options.select_by_value('VB')
            browser.find_element_by_id('submit_button').click()
            break
        except Exception:
            time.sleep(1)


#
def download_file():
    """
    Download the data file from the TNC website
    """
    while not browser.find_elements_by_id('sonuc_paneli'):
        time.sleep(1)

    j = 0
    while (not browser.find_elements_by_id('dizilim_yakinlik_data_tablosu')) or\
            not browser.find_elements_by_class_name('odd'):

        time.sleep(1)
        j += 1
        if j >= 10:
            raise Exception

    attmpt = 0
    time.sleep(5)

    while True:
        try:
            attmpt += 1
            browser.find_elements_by_css_selector('.buttons-csv')[1].click()
            time.sleep(2)
            break
        except Exception:
            time.sleep(1)

        if attmpt >= 5:
            raise Exception


def main(query_terms, start=0, end=-1):
    """
    Open browser. Sign in into a TNC account. Iteratively submit queries on the
    TNC based on verbs. Download data file of the results of each query.
    Data files will be in the browser's default download folder.
    :param query_terms: list of query terms
    :param start: index of first term to query on
    :param end: index of last term to query on
    """
    if end == -1:
        end = len(query_terms)

    # Open query page
    browser.maximize_window()
    browser.get(url_1)
    sign_in()

    # Submit query and download TSV file
    i = 0
    for search_term in query_terms[start:end]:
        try:
            print('Starting query {0}: '.format(start + i), search_term)
            browser.get(url_2)
            open_query()
            submit_query(search_term)
            download_file()
            print('Done: ', search_term)
        except Exception:
            # Warn about problem with query, create a file for indication
            print('Problem with query: ', search_term)
            decoy_file = open(f'Problem with query_{i}_{search_term}.txt', 'w')
            decoy_file.close()
        i += 1

    browser.close()


if __name__ == '__main__':
    # Command line arguments
    parse = argparse.ArgumentParser(description='Get query results from TNC')

    parse.add_argument('-s', '--start', help='Start index on query term list',
                       default=0, type=int)

    parse.add_argument('-e', '--end', help='End index on query term list',
                       default=-1, type=int)

    parse.add_argument('-f', '--file', help='File path of query terms',
                       default='query_terms.txt', type=str)

    parse.add_argument('-b', '--browser', help='Browser to use',
                       default='safari', type=str, choices=['safari'])

    parse.add_argument('-u', '--username', help='Username on TNC',
                       required=True, type=str)

    parse.add_argument('-p', '--password', help='Password of TNC account',
                       required=True, type=str)

    args = parse.parse_args()

    # TNC-related information
    url_1 = "https://v3.tnc.org.tr/login"
    url_2 = "https://v3.tnc.org.tr/basic-query"
    email = args.username
    password = args.password

    # Browser to use
    browsers = {'safari': webdriver.Safari()}
    browser = browsers[args.browser]

    # Get query terms
    with open(args.file, 'r') as f:
        query_terms = f.read().split('\n')

    # Run queries
    main(query_terms, start=args.start, end=args.end)

    exit(0)
