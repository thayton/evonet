#!/usr/bin/env python

import re
import string
import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

PLUGINFO = {
    'url': 'https://www.shine.com.au/meet-the-team/'
}

class ShineScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])
        
        s = BeautifulSoup(self.driver.page_source)
        r = re.compile(r'^/en/ourpeople/[^/]+$')
        x = {'class': 'team-member'}
        y = {'class': 'details'}

        for a in s.findAll('article', attrs=x):
            d = a.find('div', attrs=y)

            title = a.small.text.strip().lower()
            if 'partner' not in title and 'associate' not in title:
                continue

            # URL, name, job title and location
            person = {}
            person['name'] = d.a.text.strip()
            person['url'] = urlparse.urljoin(self.driver.current_url, a.a['href'])
            person['job_title'] = title
            person['location'] = ''
            print person

        self.driver.quit()

def get_scraper():
    return ShineScraper()

if __name__ == '__main__':
    scraper = ShineScraper()
    scraper.scrape()        
