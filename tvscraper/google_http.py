#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, re
from pprint import pprint


from google import google # project: Google-Search-API

class GoogleHTTP():

    def __init__(self, data):

        self._data = data

    @property
    def data(self): return self._data

    def _query(self, query, **kwargs):
        if kwargs.has_key('site'): query = "site:{} {}".format(kwargs['site'], query)
        return query

    def search(self, query, **kwargs):

        query = self._query(query, **kwargs)
        scraper = {'query': query, 'result': []}; found = 0

        gs = google.search(query, lang='de')
        if gs:
            for entry in gs:
                found += 1
                result = { 'name': entry['name'],
                           'link': entry['link'],
                           'description': entry['description'],
                           'url': entry['link'] }
                scraper['result'].append(result)

        scraper = { 'GoogleHTTP': scraper}
        self._data['scraper'] = scraper
        return found

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

    sites = [
        {
            'site':'www.imdb.com',
            'query': ['title','subtitle']
        },
        {
            'site': 'www.thetvdb.com',
            'query': ['title','subtitle']
        },
        {
            'site': '',
            'query': ['title','subtitle']
        }
    ]

    # for entry in data:
    #     for site in sites:
    #         query = site['site']
    #         for key in site['query']:
    #             query = query + " " + entry[key]
    #         query = query.strip()
    #         if GoogleHTTP(entry).search(query):
    #             pprint(entry)
    #         else:
    #             print 'Not found!'

    # Empty ???
    entry = data[0]
    query = "site:thetvdb.com {0} {1}".format(entry['title'], entry['subtitle'])

    # OK => Terra X not found at imdb.com!
    #entry = data[0]
    #query = "site:imdb.com {0} {1}".format(entry['title'], entry['subtitle'])

    # OK!
    #entry = data[1]
    #query = "site:imdb.com {0} {1}".format(entry['title'], entry['subtitle'])

    # Empty ???
    entry = data[1]
    #query = "site:thetvdb.com {0} {1}".format(entry['title'], entry['subtitle'])
    #query = "{0} {1}".format(entry['title'], entry['subtitle'])

    GoogleHTTP(entry).search(query)

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()





if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion
