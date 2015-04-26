#!/usr/bin/env python                                                                                                                                                                
"""
Python script for scraping the people from http://incelaw.com/en/ourpeople
"""

__author__ = 'Todd Hayton'

import re
import string
import urlparse
import requests

from bs4 import BeautifulSoup, Comment, Tag

PLUGINFO = {
    'url': 'http://incelaw.com/en/ourpeople/search-results'
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

class InceLawScraper(object):
    def __init__(self):
#        self.url = 'http://www.InceLaw.com/people'
        self.url = 'http://incelaw.com/en/ourpeople/search-results'
        self.headers = { 'User-agent': 
                         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7' }

    def scrape(self):
        #
        # r = requests.get(self.url, headers=self.headers)
        # print r['cookies']
        #
        # 
        # $('.search-surname a:not(.inactive)').on("click", function () {
        #   var letter = $(this).text();
        #   if (letter != '') {
        #     // Need to remove the onunload event from the page if it is set, otherwise it will overwrite our cookie data
        #     $(window).unbind('beforeunload');
        #     SaveStateWithParams('op_data', '', '', '', '', letter.toString(), '', '1', '', letter);
        #     var url = $("#SearchResultPage").val();
        #     window.location.href = url;
        #   }
        # });
        #
        #
        #  SaveStateWithParams('op_data',              // cookie_name
        #                      '',                     // search_terms
        #                      '',                     // sector
        #                      '',                     // location
        #                      '',                     // position
        #                      letter.toString(),      // letter
        #                      '',                     // type_filters
        #                      '1',                    // page_num
        #                      '',                     // sort_field
        #                      letter                  // letter_search
        #  );
        #
        # <input type="hidden" id="cookiename" value="op_data" />
        #
        # function SaveStateWithParams(cookie_name, search_terms, sector, location, position, letter, type_filters, page_num, sort_field, letter_search) {
        #   var cookie_fields;
        #   if (cookie_name == 'filter_data' || cookie_name == 'ok_data') {
        #     cookie_fields = new Array(page_num, location, sector, search_terms, type_filters);
        #   } else if (cookie_name == 'op_data') {
        #     cookie_fields = new Array(page_num, location, sector, search_terms, position, sort_field, letter_search);
        #   }
        # 
        #   var cookie_data = (cookie_fields).join(DELIM);
        #   $.cookie(cookie_name, cookie_data, {expires: 7,path: '/'});
        # }
        #
        # DELIM is '|' therefore cookie_fields for page 1 search for surname 'Q'
        #
        # cookie_fields=Array([1,,,,,,Q])
        # cookie_name=cookie_data is op_data=1||||||Q
        #

        #
        # for letter in string.uppercase[0]:
        #   pageno = 2
        #   d['page_num'] = 1
        #   d['letter_search'] = 'A'
        #   '|||||||'.join(d.values())
        #
        cookie = {}
        cookie_data = {}
        cookie_data['page_num'] = '1'

        for letter in string.uppercase:
            cookie_data['letter_search'] = letter

            pageno = 2
            url = self.url

            while True:
                cookie['op_data'] = '||||||'.join(cookie_data.values())
                resp = requests.get(url, headers=self.headers, cookies=cookie)

                s = BeautifulSoup(resp.text)
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
                    person['url'] = urlparse.urljoin(resp.url, a['href'])
                    person['job_title'] = last_span_split[0]  
                    person['location'] = last_span_split[1] if len(last_span_split) > 1 else ''
                    print person

                # Pagination
                r = re.compile(r'^/en/ourpeople/search-results\?page=%d' % pageno)
                a = s.find('a', href=r)

                if not a:
                    break

                pageno += 1
            
                url = urlparse.urljoin(resp.url, a['href'])
                cookie_data['page_num'] = '0'

def get_scraper():
    return InceLawScraper()

if __name__ == '__main__':
    scraper = InceLawScraper()
    scraper.scrape()


