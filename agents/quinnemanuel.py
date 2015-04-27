#!/usr/bin/env python

import re
import time
import string
import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

PLUGINFO = {
    'url': 'http://www.quinnemanuel.com/attorneys'
}

class QuinnEmanuelScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])
        
        for letter in string.uppercase:
            elem = self.driver.find_element_by_xpath("//a[text()='%s']" % letter)
            elem.click()

            #
            # A little wait so that <ul id=ulAttorney> contents have time 
            # to load. 
            #
            time.sleep(3)

            s = BeautifulSoup(self.driver.page_source)
            ul = s.find('ul', id='ulAttorney')

            for li in ul.findAll('li'):
                div = { x['class'][0]: x for x in li.a.findAll('div') }

                # URL, name, job title and location
                person = {}
                person['name'] = div['name'].text
                person['url'] = urlparse.urljoin(self.driver.current_url, li.a['href'])
                person['job_title'] = div['associalAs'].text
                person['location'] = div['location'].text
                print person

        self.driver.quit()

def get_scraper():
    return QuinnEmanuelScraper()

if __name__ == '__main__':
    scraper = QuinnEmanuelScraper()
    scraper.scrape()        
