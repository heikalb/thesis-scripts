"""
Make lemma-based queries on the TNC web interface based on a given list of lemmas
"""
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import Select
import time

search_terms = open('query_terms.txt', 'r').read().split('\n')
url_1 = "https://v3.tnc.org.tr/login"
url_2 = "https://v3.tnc.org.tr/basic-query"
email = 'heikal93@gmail.com'
password = 'kolipoki'
browser = webdriver.Safari()


# Sign into a TNC account
def sign_in():
    while True:
        try:
            browser.find_element_by_css_selector('input[placeholder=Email]').send_keys(email)
            browser.find_element_by_name('password').send_keys(password)
            browser.find_element_by_css_selector('input[type=submit]').click()
            break
        except NoSuchElementException:
            time.sleep(2)


# Open the page with the lemma-based queryy
def open_query():
    while True:
        try:
            browser.find_elements_by_css_selector('.btn-group.col-md-12 .btn.btn-default')[1].click()
            break
        except NoSuchElementException:
            time.sleep(2)


# Submit query
def submit_query(search_term):
    while True:
        try:
            browser.find_element_by_id('query').send_keys(search_term)
            pos_options = Select(browser.find_element_by_id('type'))
            pos_options.select_by_value('VB')
            browser.find_element_by_id('submit_button').click()
            break
        except NoSuchElementException:
            time.sleep(2)


# Download data file
def download_file():
    while True:
        try:
            browser.find_elements_by_css_selector('.buttons-csv')[1].click()
            break
        except NoSuchElementException:
            time.sleep(2)
        except IndexError:
            time.sleep(2)


def main(starting_index=0):
    # Open query page
    browser.maximize_window()
    browser.get(url_1)
    sign_in()
    time.sleep(5)

    for search_term in search_terms[starting_index:]:
        browser.get(url_2)
        print('Starting query: ', search_term)
        # Choose correct query type
        open_query()
        # Fill in search parameters
        submit_query(search_term)
        # Download TSV file
        download_file()
        print('Done: ', search_term)

    browser.close()


if __name__ == '__main__':
    main(0)
    exit()
