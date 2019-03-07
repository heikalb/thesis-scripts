from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


import time
search_terms = open('query_terms.txt', 'r').read().split('\n')


def main():
    url_1 = "https://v3.tnc.org.tr/login"
    url_2 = "https://v3.tnc.org.tr/basic-query"
    email = 'heikal93@gmail.com'
    password = 'kolipoki'

    # Open query page
    browser = webdriver.Safari()

    for search_term in search_terms:
        browser.get(url_1)
        browser.maximize_window()

        while True:
            try:
                browser.find_element_by_css_selector('input[placeholder=Email]').send_keys(email)
                browser.find_element_by_name('password').send_keys(password)
                browser.find_element_by_css_selector('input[type=submit]').click()
                break
            except NoSuchElementException:
                time.sleep(2)

        time.sleep(5)
        browser.get(url_2)
        # Choose correct query type
        while True:
            try:
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable(browser.find_element_by_id('bicim-bassozcuk')))
                # WebDriverWait(browser, 10).until(EC.element_to_be_clickable(By.ID))
                # browser.find_elements_by_class_name('btn-default')[1].click()
                # browser.find_elements_by_css_selector('div[data-toggle=buttons]')
                print(browser.find_element_by_id('bicim-bassozcuk').is_displayed())
                print(browser.find_element_by_id('bicim-bassozcuk').is_enabled())
                print(browser.find_element_by_id('bicim-bassozcuk').is_selected())
                browser.find_element_by_id('bicim-bassozcuk').click()
                break
            except NoSuchElementException:
                time.sleep(2)

        # Fill in search parameters
        while True:
            try:
                browser.find_element_by_id('query').send_keys(search_term)
                pos_options = Select(browser.find_element_by_id('type'))
                pos_options.select_by_value('VB')
                browser.find_element_by_id('submit_button').click()
                break
            except NoSuchElementException:
                time.sleep(2)

        # Download TSV file
        while True:
            try:
                browser.find_element_by_css_selector('.btn btn-default.buttons-csv.buttons-html5 btn-sm').click()
                break
            except NoSuchElementException:
                time.sleep(2)

    browser.close()


if __name__ == '__main__':
    main()
    exit()
