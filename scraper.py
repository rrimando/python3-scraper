#!/usr/bin/env python3
# coding=utf-8
import sys
"""
SCRAPE URLS FOR CONTENT
"""
import urllib
import datefinder

from datetime import datetime
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import Request, urlopen  # Web client

now = datetime.now()

class Scraper():

    def __init__(self):
        print('CONFIGURING SCRAPER')

        self.counter = 1

        # File modification 

        self.config = [
            {
                'url': 'https://www.google.com/search?q=test',
                'targets': [{
                    'container': 'results',
                    'element': 'a',
                    'attribute': 'links', # or text
                    'target': {}, # {"<selector>": "<name>"},
                }]
            },
            # {
            #     'url': 'https://www.google.com/search?q=test',
            #     'targets': [{
            #         'container': 'results',
            #         'element': 'a',
            #         'attribute': 'links', # or text
            #         'target': {}, # {"<selector>": "<name>"},
            #     }]
            # },
        ]

    def start(self):

        print('STARTING SCRIPT')

        parsed_data = {}

        for configuration in self.config:      
            print("(" + str(self.counter) + ")FETCHING : " + configuration['url'])

            config_targets = configuration['targets']
            
            try:
                client = Request(configuration['url'], headers={'User-Agent': 'Mozilla/5.0'})

            except urllib.error.HTTPError as e:
                if e.code == 404 or e.code == 403:

                    print('RESPONSE WAS ' + str(e.code))
                    print('PAGE DOES NOT EXIST!')
                    continue   
            else:
                pagecontent = urlopen(client).read()
                urlopen(client).close()

                # Parse Data
                for data_target in config_targets:

                    # Grab Data
                    if data_target['container']:
                        parsed_data[data_target['container']] = self.parse(pagecontent, data_target['element'], data_target['target'], data_target['attribute']) 

                    else:
                        print('PAGE COULD NOT BE REACHED OR WAS REDIRECTED')

                    self.counter += 1

        print('ENDED SCRIPT RUN')

        return parsed_data


    def getFileContents(self, fileTarget):
        urls = []

        for line in open(fileTarget, 'r'):
            urls.append(line.strip()) 

        return urls

    
    def parseHTML(self, html, element, target, target_attribute='text', html_format=False):
        if target_attribute == 'text':
            try:
                result = html.find(element, target).prettify().encode('utf8') if html_format else html.find(element, target).getText().encode('utf8')
            
                return result if result and result is not None else ''

            except:
                return ''

        if target_attribute == 'links':
            links = []

            for a in html.find_all(element, href=True):
                links.append(a['href'])

            return links


    def parse(self, html, element, target, attribute):

        html_soup = soup(html, "html.parser")

        target_content = self.parseHTML(html_soup, element, target, attribute)
        # variable = self.parseHTML(html_soup, '<element>', {"<selector>": "<class nam>"}, True)
        return target_content

import pprint

if __name__ == '__main__':
    scraper = Scraper()
    results = scraper.start()

    print('---------------------------------------')
    pprint.pprint(results)