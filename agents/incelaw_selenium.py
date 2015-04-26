#!/usr/bin/env python

import re
import string
import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

PLUGINFO = {
    'url': 'http://incelaw.com/en/ourpeople/'
}

class InceLawScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])
        
        for letter in string.uppercase:
            elem = self.driver.find_element_by_xpath("//a[text()='%s']" % letter)
            elem.click()

            pageno = 2

            while True:
                s = BeautifulSoup(self.driver.page_source)
                r = re.compile(r'^/en/ourpeople/[^/]+$')
                x = {'class': 'person-link', 'href': r}

                for a in s.findAll('a', attrs=x):
                    if a.img:
                        continue

                    h2 = a.findParent('h2')
                    sp = h2.findAll('span')
                    last_span_split = ['%s' % z.strip() for z in sp[-1].text.rsplit(',', 1)]

                    # URL, name, job title and location
                    person = {}
                    person['name'] = a.text.strip()
                    person['url'] = urlparse.urljoin(self.driver.current_url, a['href'])
                    person['job_title'] = last_span_split[0]  
                    person['location'] = last_span_split[1] if len(last_span_split) > 1 else ''
                    print person

                # Pagination
                try:
                    next_page_elem = self.driver.find_element_by_xpath("//a[text()='%d']" % pageno)
                except NoSuchElementException:
                    break # no more pages

                next_page_elem.click()
                pageno += 1

        self.driver.quit()

if __name__ == '__main__':
    scraper = InceLawScraper()
    scraper.scrape()        
