#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, re
from pprint import pprint

from tvscraper import Scraper
from googlesearch import GoogleSearch   # pip package

class GoogleScraper(Scraper):

    config = {

        'none' : { 'query': ""},
        'imdb' : { 'query': "site:imdb.com"},
        'tvdb' : { 'query': "site:thetvdb.com" }
    }

    def __init__(self, data):
        Scraper.__init__(self, data)

    def _parse_tvdb_result(self, result):

        found = False
        match = re.search('(.*): Season (\w+) Episode', result['titleNoFormatting'])
        if match:
            self.data['show'] = match.group(1)
            self.data['season_name'] = match.group(2)
            found = True

        match = re.search('tab=season&seriesid=(\d+)&seasonid=(\d+)&lid=(\d+)', result['unescapedUrl'])
        if match:
            self.data['tvdb_series'] = match.group(1)
            self.data['tvdb_season'] = match.group(2)
            self.data['tvdb_lid'] = match.group(3)
            self.data['tvdb_url'] = result['unescapedUrl']
            found = True
        else:
            match = re.search('tab=seasonall&id=(\d+)&lid=(\d+)', result['unescapedUrl'])
            if match:
                self.data['tvdb_series'] = match.group(1)
                self.data['tvdb_lid'] = match.group(2)
                self.data['tvdb_url'] = result['unescapedUrl']
                found = True

        return TvDbScraper(self.data).search()


# region __Main__

def main():
    pass

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion
