#!/usr/bin/env python                                                                                                                                                                
"""
Python script for scraping the people from http://www.charlesrussellspeechlys.com/people/
"""

__author__ = 'Todd Hayton'

import re
import json
import string
import urlparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup, Comment, Tag

PLUGINFO = {
    'url': 'http://www.charlesrussellspeechlys.com/people/'
}

class CharlesRussellSpeechlysScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])

        for letter in string.uppercase:
            elem = self.driver.find_element_by_xpath("//a[text()='%s']" % letter)
            elem.click()

            prev_ppl_count = 0

            while True:
                #
                # Wait until the loader goes away (display: none) to determine when
                # the page has finished loading
                #
                #print self.driver.find_element_by_id('lastPostsLoader').is_displayed()

                wait = WebDriverWait(self.driver, 10)
                wait.until(lambda driver: driver.find_element_by_id('lastPostsLoader').is_displayed() == False)

                #print self.driver.find_element_by_id('lastPostsLoader').is_displayed()

                #
                # We know there are no more results to be loaded when the total number 
                # of people elements does not change
                #
                s = BeautifulSoup(self.driver.page_source)
                r = re.compile(r'pnlResults$')
                d = s.find('div', id=r)
                x = { 'class': re.compile(r'block|about') }

                next_ppl_count = len(d.findAll('div', attrs=x))
                if next_ppl_count == prev_ppl_count:
                    break

                prev_ppl_count = next_ppl_count

                #
                # Now trigger scrolling and wait until results loaded. 
                #
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #
            # By this point we should have 'scrolled' to the bottom of the page
            # and all the results should be loaded into our pnlResults div
            #
            for b in d.findAll('div', attrs=x):
                person = {}
                person['name'] = b.h5.a.text.strip()
                person['url'] = urlparse.urljoin(self.driver.current_url, b.h5.a['href'])
                person['job_title'] = b.h6.text
                person['location'] = ''
                print person
                
def get_scraper():
    return CharlesRussellSpeechlysScraper()

if __name__ == '__main__':
    scraper = CharlesRussellSpeechlysScraper()
    scraper.scrape()

