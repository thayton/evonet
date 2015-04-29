#!/usr/bin/env python

import re
import string
import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

PLUGINFO = {
    'url': 'https://www.maddocks.com.au/our-people/'
}

class MaddocksScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])
        
        pageno = 2

        while True:
            s = BeautifulSoup(self.driver.page_source)
            r = re.compile(r'/our-people/[^/]+/$')
            x = {'class': 'link--person', 'href': r}

            for a in s.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                title = td[1].contents[-1]

                # URL, name, job title and location
                person = {}
                person['name'] = a.text.strip()
                person['url'] = urlparse.urljoin(self.driver.current_url, a['href'])
                person['job_title'] = getattr(title, 'text', title)
                person['location'] = ''
                print person

            # Pagination
            try:
                next_page_elem = self.driver.find_element_by_xpath("//a[text()='%d']" % pageno)
            except NoSuchElementException:
                break # no more pages

            next_page_elem.click()
            pageno += 1

        self.driver.quit()

def get_scraper():
    return MaddocksScraper()

if __name__ == '__main__':
    scraper = MaddocksScraper()
    scraper.scrape()        
