#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    filter tv shows and episodes at TheTVDB
"""

__version__ = "0.9"
__author__ = 'bst'

import sys, json, re
from pprint import pprint


from imdbscraper import IMDbScraper
from tvdbscraper import TvDbScraper
from bing_api import BingAPI
from google_cse import GoogleCSE


class TvScraper:

    def __init__(self, data=None):

        self._data = data if data else {}

    @property
    def data(self): return self._data

    @property
    def isTv(self): return self.data['type'] == 'tv'

    '''
    http://www.imdb.com/title/tt1172564/

    http://thetvdb.com/?tab=episode&seriesid=126301&seasonid=510424&id=4625859&lid=14
    http://thetvdb.com/?tab=season&seriesid=126301&seasonid=510424&lid=14
    http://thetvdb.com/?tab=seasonall&id=126301&lid=14
    '''

    def _check_scraper_result(self, scraper):

        scraper = self.data['scraper'][scraper]

        for result in scraper['result']:

            link = result['link']

            if re.search('thetvdb\.com/\?tab=', link):
                match = re.match('.*thetvdb.com/\?tab=episode&seriesid=(\d+)&seasonid=(\d+)&id=(\d+)', link)
                if match:
                    self.data['tvdb_series'] = match.group(1)
                    self.data['tvdb_season'] = match.group(2)
                    self.data['tvdb_episode'] = match.group(3)
                    return TvDbScraper(self.data).search()
                    # return True
                else:
                    match = re.match('.*thetvdb.com/\?tab=season&seriesid=(\d+)&seasonid=(\d+)',link)
                    if match:
                        self.data['tvdb_series'] = match.group(1)
                        self.data['tvdb_season'] = match.group(2)
                    else:
                        match = re.match('.*thetvdb\.com/\?tab=seasonall&id=(\d+)',link)
                        if match:
                            self.data['tvdb_series'] = match.group(1)

            elif re.match('.*imdb.com/title', link):
                match = re.match('.*imdb.com/title/tt(\d+)',link)
                if match:
                    self.data['imdb_tt'] = match.group(1)
                    return IMDbScraper(self.data).search()
            else:
                print "%s [%s]" % (result['name'], result['link'])

    def search(self, **kwargs):

        self._data.update(**kwargs)

        if self.data.has_key('query'):
            query = self.data['query']
        else:
            query = "%s %s" % (self.data['title'], self.data['subtitle'])

        if self.isTv:

            if BingAPI(self.data).search(query, site='thetvdb.com'):
                if self._check_scraper_result('BingAPI'): return self.data

            if BingAPI(self.data).search(query, site='imdb.com'):
                if self._check_scraper_result('BingAPI'): return self.data

            # if BingAPI(self.data).search(query):
            #    if self._check_scraper_result('BingAPI'): return True

            if GoogleCSE(self.data).search(query):
                if self._check_scraper_result('GoogleCSE'): return self.data


        return None

# region __main__

def main():

    data = [
        {
            "title": "Der Darß - Küste der Kraniche",
            "subtitle": ""
        },
        # {
        #     "title": "Terra X",
        #     "subtitle": "Phantome der Tiefsee (2) - Monsterhaie",
        # },
        # {
        #     "title": "Mord mit Aussicht",
        #     "subtitle": "Vatertag",
        # }
    ]

    for entry in data:
        query = "%s %s" % (entry['title'], entry['subtitle'])
        result = TvScraper().search(query=query, type='tv')
        print json.dumps(result, indent=4, ensure_ascii=False, encoding='utf-8')

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion

'''

        self._config = {

            'imdb' : {
                'class': IMDbScraper,
                'query': "%s %s" % (data['title'], data['subtitle']),
                'site': "site:imdb.com"},
            'tvdb' : {
                'class': TvDbScraper,
                'site': "thetvdb"}
        }

        sites = kwargs['site'] if kwargs.has_key('site') else ['tvdb']
        # keys = kwargs['keys'] if kwargs.has_key('keys') else ['title', 'subtitle']

        for site in sites:
            config = self.config[site]
            if config['class'](self.data).search('tv'):
                return


'''