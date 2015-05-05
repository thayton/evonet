#!/usr/bin/env python                                                                                                                                                                
"""
Python script for scraping the people from http://www.weightmans.com/our-people/
"""

__author__ = 'Todd Hayton'

import re
import urlparse
import mechanize

from bs4 import BeautifulSoup, Comment, Tag
from mechanize import ControlNotFoundError

PLUGINFO = {
    'url': 'http://www.weightmans.com/our-people/'
}

def soupify(page):
    s = BeautifulSoup(page)

    # Remove unwanted tags
    tags = s.findAll(lambda tag: tag.name == 'script' or \
                                 tag.name == 'style')
    for t in tags:
        t.extract()
        
    # Remove comments
    comments = s.findAll(text=lambda text:isinstance(text, Comment))
    for c in comments:
        c.extract()

    return s

def select_form(form):
    '''
    Select Search by name form at http://www.weightmans.com/our-people/
    '''
    try:
        form.find_control('PartnerId') 
    except ControlNotFoundError:
        return False
            
    return True

class WeightmansScraper(object):
    def __init__(self):
        self.url = 'http://www.weightmans.com/our-people/'
        self.br = mechanize.Browser()
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def get_name_items(self):
        self.br.open(self.url)
        self.br.select_form(predicate=select_form)

        items = self.br.form.find_control('PartnerId').get_items()
        return items

    def scrape_person(self, name_item):
        self.br.open(self.url)
        self.br.select_form(predicate=select_form)
        self.br.form['PartnerId'] = [ name_item.name ]
        self.br.submit()

        s = soupify(self.br.response().read())
        x = {'class': 'maincontent-full'}
        d = s.find('div', attrs=x)

        #
        # <URL, name, job title and location>
        #
        # Return a blank if there is no job title or location, the only required fields are URL and name
        #
        person = {}
        person['name'] = name_item.attrs.get('label')
        person['url'] = self.br.geturl()
        person['job_title'] = ''
        person['location'] = ''
        print person

    def scrape(self):
        name_items = self.get_name_items()
        for name_item in name_items:
            #print 'scraping', name_item
            self.scrape_person(name_item)

def get_scraper():
    return WeightmansScraper()

if __name__ == '__main__':
    scraper = WeightmansScraper()
    scraper.scrape()


