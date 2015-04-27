#!/usr/bin/env python

import re
import string
import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

PLUGINFO = {
    'url': 'http://www.cadwalader.com/find/professionals/'
}

class CadwaladerScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])
        
        s = BeautifulSoup(self.driver.page_source)
        x = {'class': 'data pro-results'}
        r = re.compile(r'/offices/[^/]+$')

        for t in s.findAll('table', attrs=x):
            th = t.tr.th
            td = t.tr.findAll('td')

            n = ' '.join(['%s' % n for n in th.a.text.split()])
            l = td[-1].find('a', href=r)

            # URL, name, job title and location
            person = {}
            person['name'] = n
            person['url'] = urlparse.urljoin(self.driver.current_url, th.a['href'])
            person['job_title'] = th.div.text.strip()
            person['location'] = l.text.strip()
            print person

        # 
        # XXX The pagination if a facade in the browser- inspect the network data
        # and you'll see that all the names are received in the first request and
        # client side javascript paginates it for readability
        #
        self.driver.quit()

def get_scraper():
    return CadwaladerScraper()

if __name__ == '__main__':
    scraper = CadwaladerScraper()
    scraper.scrape()        
