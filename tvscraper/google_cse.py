#!/usr/bin/env python
# encoding: utf-8

import sys
import urllib
import urlparse
import requests



import json
from collections import OrderedDict

from pprint import pprint

class GoogleCSE(object):

    def __init__(self, data):

        self._search_engine_id = '018128605702257391833:boy8mbur1jk'
        self._api_key = 'AIzaSyB4CUdOTi6xdyi8twd40588-cAEY7lb0B8'
        self._data = data

    def _url(self, query, **kwargs):

        params = OrderedDict([
            ('cx', self._search_engine_id),
            ('key', self._api_key),
            ('num', '10'),
            ('googlehost', 'www.google.de'),
            #('siteSearch', site),
            #('gss', '.com'),
            #('rsz', '10'),
            #('oq', query),
            ('q', query.encode('utf-8')),
            ('filter', '0'),  # duplicate content filter, 1 | 0
            ('safe', 'off'),  # strict | moderate | off
        ])

        return 'https://www.googleapis.com/customsearch/v1?{}'.format(
            urllib.urlencode(params))

    def search(self, query, **kwargs):

        url = self._url(query, **kwargs)
        scraper = {'query': query, 'url': url, 'result': []}; found = 0

        response = requests.get(url)

        if response:
            content = json.loads(response.content)
            if response.status_code == 200:
                if content.has_key('items'):
                    results = content['items']
                    # print json.dumps(results, indent=4, ensure_ascii=False, encoding='utf-8')
                    for entry in results:
                        found += 1
                        result = { 'name': entry['title'],
                                   'link': entry['link'],
                                   'url': entry['formattedUrl']}

                        scraper['result'].append(result)
                scraper = { 'GoogleCSE': scraper}
                self._data['scraper'] = scraper

            else:
                print "Request returned with [%s] %s!" % (response.status_code, response.text)

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

    entry = data[0]
    query = "{0} {1}".format(entry['title'], entry['subtitle'])

    if GoogleCSE(entry).search(query):
        pprint(entry['scraper'])
    else:
        print "No result for [%s]" % query


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion