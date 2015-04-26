#!/usr/bin/env python                                                                                                                                                                
"""
Python script for scraping the people from http://www.trowers.com/people/results/
"""

__author__ = 'Todd Hayton'

import re
import urlparse
import mechanize

from bs4 import BeautifulSoup, Comment, Tag
from mechanize import ControlNotFoundError

PLUGINFO = {
    'url': 'http://www.trowers.com/people'
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
    Select Surnames search form at http://www.trowers.com/people
    '''
    return form.attrs.get('action', None) == '/people/results/'

class TrowersScraper(object):
    def __init__(self):
        self.url = 'http://www.trowers.com/people'
        self.br = mechanize.Browser()
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape(self):
        self.br.open(self.url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            x = {'summary': 'People: search results'}
            t = s.find('table', attrs=x)

            r = re.compile(r'^/people/[^/]+/$')
            x = {'class': 'more', 'href': r}

            for a in t.findAll('a', attrs=x):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                # URL, name, job title and location
                person = {}
                person['name'] = a.text.strip()
                person['url'] = urlparse.urljoin(self.br.geturl(), a['href'])
                person['job_title'] = td[-2].text.strip()
                person['location'] = td[-1].text.strip()
                print person

            # Pagination
            try:
                self.br.follow_link(self.br.find_link(text='%d' % pageno))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break # fin- no more pages

def get_scraper():
    return TrowersScraper()

if __name__ == '__main__':
    scraper = TrowersScraper()
    scraper.scrape()


