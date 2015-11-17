#!/usr/bin/env python
# encoding: utf-8

import sys
import urllib, requests
from collections import OrderedDict

import json

class BingAPI():

    def __init__(self, data):
        # azure data market account key
        self._key = 'XVXp5LAxtPxNAt36DavCzWtbHKX8I1sseAUK2om1Diw='
        self._data = data

    def _request_url(self, query, **kwargs):

        if kwargs.has_key('site'): query = "site:{} {}".format(kwargs['site'], query)

        params = OrderedDict([
            ('Query', "'{}'".format(query)),
            ('$top', 10),
            ('$skip', 0),
            ('$format', 'json')
        ])

        return 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web?{}'.format(urllib.urlencode(params))

    def search(self, query, **kwargs):

        url = self._request_url(query, **kwargs)
        scraper = {'query': query, 'result': []}
        if kwargs.has_key('site'): scraper['site'] = kwargs['site']
        found = 0

        response = requests.get(url, auth=(self._key,self._key))

        if response:
            scraper['response'] = response.status_code
            content = json.loads(response.content)
            if response.status_code == 200:
                results = content['d']['results']
                # print json.dumps(results, indent=4, ensure_ascii=False, encoding='utf-8')
                for entry in results:
                    found += 1
                    result = {'name': entry['Title'],'link': entry['Url']}
                    scraper['result'].append(result)
            else:
                pass
                # print "Request returned with [%s] %s!" % (response.status_code, response.text)
            self._data['scraper'].update({'BingAPI': scraper})
        return found

# region __main__

def main():

    data = [
        {
            "title": "Der Darß - Küste der Kraniche",
            "subtitle": "",
        },
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
            'site':'site:imdb.com',
            'query': ['title','subtitle']
        },
        {
            'site': 'thetvdb.com',
            'query': ['title']
        },
        {
            'site': '',
            'query': ['title','subtitle']
        }
    ]

    # OK!
    #entry = data[0]
    #query = "site:thetvdb.com {0} {1}".format(entry['title'], entry['subtitle'])

    # OK => Terra X not found at imdb.com!
    # entry = data[0]
    # query = "site:imdb.com {0} {1}".format(entry['title'], entry['subtitle'])

    # OK!
    #entry = data[1]
    #query = "site:imdb.com {0} {1}".format(entry['title'], entry['subtitle'])

    # OK
    entry = data[0]
    #query = "site:thetvdb.com {0} {1}".format(entry['title'], entry['subtitle'])
    query = "{0} {1}".format(entry['title'], entry['subtitle'])

    BingAPI(entry).search(query, site='imdb.com')

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion


