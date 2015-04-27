#!/usr/bin/env python                                                                                                                                                                

"""
Python script for scraping the people from http://www.charlesrussellspeechlys.com/people/
"""

__author__ = 'Todd Hayton'

import re
import json
import string
import urlparse
import requests

from bs4 import BeautifulSoup, Comment, Tag

# Use selenium version now
skip = True

PLUGINFO = {
    'url': 'http://www.charlesrussellspeechlys.com/people/'
}

class CharlesRussellSpeechlysScraper(object):
    def __init__(self):
        self.first_letter_url = 'http://www.charlesrussellspeechlys.com/api/GetPeopleByFirstLetter'
        self.scrolling_url = 'http://www.charlesrussellspeechlys.com/api/GetPeopleResults'
        self.headers = { 'User-agent': 
                         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7',
                         'X-Requested-With': 'XMLHttpRequest',
                         'Content-Type': 'application/json',
                         'Accept': 'application/json, text/javascript, */*',
                         'Referer': 'http://www.charlesrussellspeechlys.com/people/'
        }

    def scrape(self):
        for letter in string.uppercase:
            payload = {'firstLetter': '%s' % letter}
            resp = requests.post(
                self.first_letter_url, 
                data=json.dumps(payload),
                headers=self.headers
            )

            #
            # Save the cookies- that's how the endless scroll is working
            # behind the scenes
            #
            cookies = resp.cookies

            while True:
                data = resp.json()['Data']
                if len(data) == 0:
                    break

                for item in data:
                    person = {}
                    person['name'] = item['PersonName']
                    person['url'] = urlparse.urljoin(resp.url, item['Url'])
                    person['job_title'] = item['Position']
                    person['location'] = ''
                    print person
                
                # Scrolling
                resp = requests.post(
                    self.scrolling_url, 
                    headers=self.headers,
                    cookies=cookies
                )

def get_scraper():
    return CharlesRussellSpeechlysScraper()

if __name__ == '__main__':
    scraper = CharlesRussellSpeechlysScraper()
    scraper.scrape()

