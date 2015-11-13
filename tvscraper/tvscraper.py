#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    filter tv shows and episodes at TheTVDB
"""

__version__ = "0.9"
__author__ = 'bst'

import sys, json, re
from pprint import pprint


class TvScraper:

    def __init__(self, data):

        from imdbscraper import IMDbScraper
        from tvdbscraper import TvDbScraper

        self._config = {

            'imdb' : {
                'class': IMDbScraper,
                'query': "%s %s" % (data['title'], data['subtitle']),
                'site': "site:imdb.com" },
            'tvdb' : {
                'class': TvDbScraper,
                'site': "site:thetvdb.com" }
        }

        self._data = data

    @property
    def data(self): return self._data

    @property
    def config(self): return self._config

    def search(self, **kwargs):

        sites = kwargs['site'] if kwargs.has_key('site') else ['tvdb']
        # keys = kwargs['keys'] if kwargs.has_key('keys') else ['title', 'subtitle']

        for site in sites:
            config = self.config[site]
            if config['class'](self.data).search('tv'):
                return


# region __main__

def main():

    data = [
        {
            "title": "Terra X",
            "subtitle": "Phantome der Tiefsee (2) - Monsterhaie",
        },
        {
            "title": "Mord mit Aussicht",
            "subtitle": "Vatertag",
        }
    ]

    for entry in data:
        if TvScraper(entry).search():
            print(entry)

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion

