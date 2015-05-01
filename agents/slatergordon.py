#!/usr/bin/env python

import re
import string
import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

PLUGINFO = {
    'url': 'https://www.slatergordon.com.au/our-people'
}

class SlaterGordonScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        self.driver.get(PLUGINFO['url'])

        #
        # XXX Can't figure out how to get rid of the 'Are you in QLD?' modal/popup
        # programatically but it seems to work even when this popup is overlayed on 
        # top of the results...
        #
        elem = self.driver.find_element_by_id('edit-submit-people-search')
        elem.click()

        wait = WebDriverWait(self.driver, 5)
        wait.until(lambda driver: driver.find_element_by_xpath('//ul[@class="pager"]'))

        pageno = 2
        
        while True:
            s = BeautifulSoup(self.driver.page_source)
            x = {'class': 'item-list'}
            d = s.find('div', attrs=x)
            r = re.compile(r'^/en/ourpeople/[^/]+$')

            for li in d.ul.findAll('li'):
                # URL, name, job title and location
                person = {}
                person['name'] = li.div.a.text.strip()
                person['url'] = urlparse.urljoin(self.driver.current_url, li.div.a['href'])
                person['job_title'] = ''
                person['location'] = ''
                print person

            # Pagination
            try:
                next_page_elem = self.driver.find_element_by_xpath("//a[text()='%d']" % pageno)
            except NoSuchElementException:
                break # no more pages

            next_page_elem.click()

            wait.until(lambda driver: driver.find_element_by_xpath('//li[@class="pager-current" and text()="%d"]'  % pageno))

            pageno += 1

        self.driver.quit()

def get_scraper():
    return SlaterGordonScraper()

if __name__ == '__main__':
    scraper = SlaterGordonScraper()
    scraper.scrape()        
