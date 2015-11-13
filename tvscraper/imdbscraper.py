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

    def search(self, type):

        ignore_titles = ['Terra X', 'heute-show']
        year = ''
        title = self.data['title']
        subtitle = self.data['subtitle']
        tokens = []

        if title in ignore_titles:
            print "Ignoring title:", title
            return False

        if type == 'tv':
            # extract an remove year from episode titles
            match = re.match('(20[01][0-9])|(19[5-9][0-9])', title)
            if match:
                year = match.group(1)
                title = re.sub(year, '', title)
            else:
                match = re.match('(20[01][0-9])|(19[5-9][0-9])', subtitle)
                if match:
                    year = match.group(1)
                    subtitle = re.sub(year, '', subtitle)

            title = re.sub('\(.*?\)','',title)
            subtitle = re.sub('\(.*?\)','',subtitle)

            tokens.append("%s %s" % (title, subtitle))
            tokens.append(subtitle)
            tokens.append(title)
            for split in reversed(re.split('[:-]', title)):
                tokens.append(split)
            for split in reversed(re.split('[:-]', subtitle)):
                tokens.append(split)

            for token in tokens:
                token = token.strip()
                if token:
                    print "Searching IMDb for episode:", token
                    if self._search(episode=token):
                        return True
            return False

    def _search(self, *args, **kwargs):

        if kwargs.has_key('imdb_tt'):
            movie = self._imdb.get_movie(kwargs['imdb_tt'])
        else:
            if kwargs.has_key('episode'):
                result = self._imdb.search_episode(kwargs['episode'])
            elif kwargs.has_key('query'):
                self.pp(kwargs)
                result = self._imdb.search_movie(kwargs['title'])

        if result:
            for movie in result:
                self.pp(movie)
                #self.pp(movie.data)
                if movie['kind'] == 'episode':
                    # basic movie information
                    self.data['imdb_tt'] = movie.movieID
                    self.data['show'] = movie.get('episode of', 'n/a')
                    self.data['episode'] = movie.get('title', 'n/a')
                    self.data['year'] = movie.get('year', 'n/a')
                    # load movie attributes
                    self._imdb.update(movie)
                    #self.pp(movie.data)
                    #self.data['show'] = movie['episode of']['title']
                    #self.data['episode'] = movie['title']
                    self.data['season'] = movie.get('season',0)
                    self.data['number'] = movie.get('episode',0)
                    return True

        return False

# region __main__

def main():

    data = {}
    IMDbScraper(data).search('tv')
    print(data)


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion

