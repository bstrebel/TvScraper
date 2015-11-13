#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, re
from pprint import pprint

# from tvscraper import Scraper

from pytvdbapi import api               # pip package
from fuzzywuzzy import fuzz             # pip package: requires python-levenshtein!


class TvDbScraper():

    def __init__(self, data):
        self._data = data
        self._tvdb = api.TVDB('4F36CC91D7116666')
        # Scraper.__init__(self, data)

    @property
    def data(self): return self._data

    @property
    def lang(self): return self.data['lang'] if self.data.has_key('lang') else 'de'

    def search(self, *args, **kwargs):

        similar = []
        matches = []
        subtitle = self.data['episode'] if self.data.has_key('episode') and self.data['episode'] else self.data['subtitle']
        title = self.data['show'] if self.data.has_key('show') and self.data['show'] else self.data['title']

        search = "%s %s" % (title, subtitle)
        result = self._tvdb.search("%s %s" % (title, subtitle), self.lang)
        pprint(result)

        result = self._tvdb.search(title, self.lang)
        pprint(result)

        result = self._tvdb.search(subtitle, self.lang)
        pprint(result)


        return False

        if result:
            self.data['show'] = show.SeriesName
            for season in show:
                for episode in season:
                    if int(episode.seasonid) == int(self.data['tvdb_season']):
                        name = episode.EpisodeName
                        if fuzz.token_set_ratio(search, name) > 90:
                            similar.append(episode)
                        if fuzz.token_set_ratio(search, name) == 100:
                            matches.append(episode)
        if len(matches) > 0:
            if len(matches) == 1:
                self.data['show'] = show.SeriesName
                self.data['episode'] = matches[0].EpisodeName
                self.data['season'] = matches[0].SeasonNumber
                self.data['number'] = matches[0].EpisodeNumber
                self.data['season'] = matches[0].SeasonNumber
                self.data['season'] = matches[0].SeasonNumber
                self.data['tvdb_episode'] =  matches[0].id
                return True
            else:
                print "Ambigious episode name [%s] for [%s]. Found multiple results ..." % (search, show.SeriesName)
                for episode in similar:
                    print episode.Name
        else:
            return False


# region __main__

def main():
    pass

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion
