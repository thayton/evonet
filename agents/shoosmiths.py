#!/usr/bin/env python

import re
import string
import urlparse

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

PLUGINFO = {
    'url': 'http://www.shoosmiths.co.uk/contact-us/people-finder-137.aspx'
}

class ShoosmithsScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])

        select = Select(self.driver.find_element_by_name('findourpeople_searchfields$lstPracticeGroups'))
        option_indexes = range(1, len(select.options))

        for index in option_indexes:
            select.select_by_index(index)
            self.driver.find_element_by_id('findourpeople_searchfields_btnSubmitSearchQuery').click()

            s = BeautifulSoup(self.driver.page_source)
            r = re.compile(r'/contact-us/cvdetails-\d+.aspx\?')
            x = { 'class': 'ui-button', 'href': r }

            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                # URL, name, job title and location
                person = {}
                person['name'] = a.text
                person['url'] = urlparse.urljoin(self.driver.current_url, a['href'])
                person['job_title'] = td[2].text
                person['location'] = ''
                print person

            #
            # Reselect otherwise we get a Stale Element exception
            #
            select = Select(self.driver.find_element_by_name('findourpeople_searchfields$lstPracticeGroups'))

        self.driver.quit()

def get_scraper():
    return ShoosmithsScraper()

if __name__ == '__main__':
    scraper = ShoosmithsScraper()
    scraper.scrape()        
