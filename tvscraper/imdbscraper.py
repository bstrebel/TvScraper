#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, json, re

import pprint

# from tvscraper import Scraper

import imdb     # IMDbPy package python-imdbpy
                # cygwin: use default windows installer and move
                # to .../site-packages (requires also python-lxml)
                # cygwin: python-setuptools && easy_install-2.7 pip

class IMDbScraper():

    def __init__(self, data):
        self._data = data
        self._imdb = imdb.IMDb()
        self._DEBUG = True
        self._pp = pprint.PrettyPrinter(indent=2,depth=8)
        # Scraper.__init__(self, data)

    @property
    def data(self): return self._data

    @property
    def DEBUG(self): return self._DEBUG

    def pp(self, obj):
        if self.DEBUG: self._pp.pprint(obj)

    def search(self, *args, **kwargs):

        if kwargs.has_key('imdb_tt'):
            movie = self._imdb.get_movie(kwargs['imdb_tt'])
        else:
            if kwargs.has_key('episode'):
                result = self._imdb.search_episode(kwargs['episode'])
            elif kwargs.has_key('title'):
                result = self._imdb.search_movie(kwargs['title'])

        if result:
            for movie in result:
                self.pp(movie)
                self.pp(movie.data)
                if movie['kind'] == 'episode':
                    # basic movie information
                    self.data['imdb_tt'] = movie.movieID
                    self.data['show'] = movie.get('episode of', 'n/a')
                    self.data['episode'] = movie.get('title', 'n/a')
                    self.data['year'] = movie.get('year', 'n/a')
                    # load movie attributes
                    self._imdb.update(movie)
                    self.pp(movie.data)
                    #self.data['show'] = movie['episode of']['title']
                    #self.data['episode'] = movie['title']
                    self.data['season'] = movie.get('season',0)
                    self.data['number'] = movie.get('episode',0)
                    return True

        return False

# region __main__

def main():

    data = {}
    IMDbScraper(data).search(title='Mord mit Aussicht - Vatertag')
    print pprint.pformat(data)


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion

