#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, re
from pprint import pprint

from googlesearch import GoogleSearch

class GoogleAPI():

    def __init__(self, data):

        self._config = {
            'none' : { 'query': ""},
            'imdb' : { 'query': "site:imdb.com"},
            'tvdb' : { 'query': "site:thetvdb.com" }
        }

        self._data = data

    @property
    def data(self): return self._data

    @property
    def config(self): return self._config

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

    def _parse_imdb_result(self, result):

        found = False
        match = re.search('http://www.imdb.com/title/tt(\d+)/', result['unescapedUrl'])
        if match:
            self.data['imdb_tt'] = match.group(1)
            self.data['imdb_url'] = result['unescapedUrl']
            #IMDbScraper(self._data).search()
            found = True
        return found

    def _parse_none_result(self, result):

        found = False
        pprint(result)
        return found




    def search(self, **kwargs):

        sites = kwargs['site'] if kwargs.has_key('site') else ['imdb','tvdb', 'none']
        keys = kwargs['keys'] if kwargs.has_key('keys') else ['title', 'subtitle']

        for site in sites:

            query = self.config[site]['query']
            for key in keys:
                query = query + " " + '"' + self.data[key] + '"'

            print "[" + query + "]"

            gs = GoogleSearch(query)

            if len(gs.result_data['results']) > 0:
                for result in gs.top_results():
                    if getattr(self, '_parse_'+site+'_result')(result):
                        return
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

    sites = [
        {
            'site':'site:imdb.com',
            'query': ['title','subtitle']
        },
        {
            'site': 'site:thetvdb.com',
            'query': ['title']
        },
        {
            'site': '',
            'query': ['title','subtitle']
        }
    ]

    for entry in data:
        GoogleAPI(entry).search()

    # for entry in data:
    #     for site in sites:
    #         query = site['site']
    #         for key in site['query']:
    #             query = query + " " + entry[key]
    #         query = query.strip()
    #         if GoogleAPI(entry).search(query):
    #             pprint(entry)
    #         else:
    #             print 'Not found!'


if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

# endregion

'''

        parms = ['search', 'site']
        opts = {}
        for count,arg in enumerate(args): opts[parms[count]] = arg
        for key,value in kwargs.items():  opts[key] = value




{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:JX6S7N3hZH4J:thetvdb.com',
 u'content': u'This season is locked at the season level and cannot be\xa0...',
 u'title': u'<b>Terra X</b>: Season 2013 Episode List - TheTVDB.com',
 u'btitleNoFormatting': u'Terra X: Season 2013 Episode List - TheTVDB.com',
 u'unescapedUrl': u'http://thetvdb.com/?tab=season&seriesid=126301&seasonid=510424&lid=14',
 u'url': u'http://thetvdb.com/%3Ftab%3Dseason%26seriesid%3D126301%26seasonid%3D510424%26lid%3D14',
 u'visibleUrl': u'thetvdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:pVuocZNVGdEJ:thetvdb.com',
 u'content': u'<b>Terra X</b>. All Seasons. Episode Number, Episode Name\xa0...',
 u'title': u'<b>Terra X</b>: Complete Episode List - TheTVDB.com',
 u'titleNoFormatting': u'Terra X: Complete Episode List - TheTVDB.com',
 u'unescapedUrl': u'http://thetvdb.com/?tab=seasonall&id=126301&lid=14',
 u'url': u'http://thetvdb.com/%3Ftab%3Dseasonall%26id%3D126301%26lid%3D14',
 u'visibleUrl': u'thetvdb.com'}


[site:imdb.com "Terra X" "Phantome der Tiefsee (2) - Monsterhaie"]

[site:thetvdb.com "Terra X" "Phantome der Tiefsee (2) - Monsterhaie"]

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:JX6S7N3hZH4J:thetvdb.com',
 u'content': u'This season is locked at the season level and cannot be\xa0...',
 u'title': u'<b>Terra X</b>: Season 2013 Episode List - TheTVDB.com',
 u'titleNoFormatting': u'Terra X: Season 2013 Episode List - TheTVDB.com',
 u'unescapedUrl': u'http://thetvdb.com/?tab=season&seriesid=126301&seasonid=510424&lid=14',
 u'url': u'http://thetvdb.com/%3Ftab%3Dseason%26seriesid%3D126301%26seasonid%3D510424%26lid%3D14',
 u'visibleUrl': u'thetvdb.com'}

{'subtitle': 'Phantome der Tiefsee (2) - Monsterhaie', 'show': u'Terra X', 'season': u'2013', 'title': 'Terra X', 'filename': '/storage/recordings/Terra X/Terra X - S2013E28 - Phantome der Tiefsee (2) - Monsterhaie.mkv', 'tvdb_season': u'510424', 'tvdb_series': u'126301'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:pVuocZNVGdEJ:thetvdb.com',
 u'content': u'<b>Terra X</b>. All Seasons. Episode Number, Episode Name\xa0...',
 u'title': u'<b>Terra X</b>: Complete Episode List - TheTVDB.com',
 u'titleNoFormatting': u'Terra X: Complete Episode List - TheTVDB.com',
 u'unescapedUrl': u'http://thetvdb.com/?tab=seasonall&id=126301&lid=14',
 u'url': u'http://thetvdb.com/%3Ftab%3Dseasonall%26id%3D126301%26lid%3D14',
 u'visibleUrl': u'thetvdb.com'}

{'subtitle': 'Phantome der Tiefsee (2) - Monsterhaie', 'show': u'Terra X', 'season': u'2013', 'title': 'Terra X', 'filename': '/storage/recordings/Terra X/Terra X - S2013E28 - Phantome der Tiefsee (2) - Monsterhaie.mkv', 'tvdb_season': u'510424', 'tvdb_series': u'126301'}


[ "Terra X" "Phantome der Tiefsee (2) - Monsterhaie"]

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:t29oK5HrsOIJ:www.zdf.de',
 u'content': u'25. Mai 2015 <b>...</b> In einem spektakul\xe4ren wissenschaftlichen Gro\xdfprojekt versuchen die \njapanische Meeresbiologen kaum bekannte Tiefsee-Haie vor die\xa0...',
 u'title': u'Phantome der Tiefsee - Monsterhaie - <b>Terra X</b> - ZDFmediathek - ZDF <b>...</b>',
 u'titleNoFormatting': u'Phantome der Tiefsee - Monsterhaie - Terra X - ZDFmediathek - ZDF ...',
 u'unescapedUrl': u'http://www.zdf.de/ZDFmediathek/beitrag/video/1951430/Phantome-der-Tiefsee---Monsterhaie',
 u'url': u'http://www.zdf.de/ZDFmediathek/beitrag/video/1951430/Phantome-der-Tiefsee---Monsterhaie',
 u'visibleUrl': u'www.zdf.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:t29oK5HrsOIJ:www.zdf.de',
 u'content': u'25. Mai 2015 <b>...</b> In einem spektakul\xe4ren wissenschaftlichen Gro\xdfprojekt versuchen die \njapanische Meeresbiologen kaum bekannte Tiefsee-Haie vor die\xa0...',
 u'title': u'Phantome der Tiefsee - Monsterhaie - <b>Terra X</b> - ZDFmediathek - ZDF <b>...</b>',
 u'titleNoFormatting': u'Phantome der Tiefsee - Monsterhaie - Terra X - ZDFmediathek - ZDF ...',
 u'unescapedUrl': u'http://www.zdf.de/ZDFmediathek/beitrag/video/1951430/Phantome-der-Tiefsee---Monsterhaie',
 u'url': u'http://www.zdf.de/ZDFmediathek/beitrag/video/1951430/Phantome-der-Tiefsee---Monsterhaie',
 u'visibleUrl': u'www.zdf.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:bQeRzK4I0_YJ:www.fernsehserien.de',
 u'content': u'\u201e<b>Terra X</b>\u201c ist eine preisgekr\xf6nte Dokumentationsreihe des ZDF, die 1982 unter \nebendiesem Namen startete und allw\xf6chentlich sonntagabends Themen von\xa0...',
 u'title': u'<b>Terra X</b> bei fernsehserien.de',
 u'titleNoFormatting': u'Terra X bei fernsehserien.de',
 u'unescapedUrl': u'http://www.fernsehserien.de/terra-x',
 u'url': u'http://www.fernsehserien.de/terra-x',
 u'visibleUrl': u'www.fernsehserien.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:bQeRzK4I0_YJ:www.fernsehserien.de',
 u'content': u'\u201e<b>Terra X</b>\u201c ist eine preisgekr\xf6nte Dokumentationsreihe des ZDF, die 1982 unter \nebendiesem Namen startete und allw\xf6chentlich sonntagabends Themen von\xa0...',
 u'title': u'<b>Terra X</b> bei fernsehserien.de',
 u'titleNoFormatting': u'Terra X bei fernsehserien.de',
 u'unescapedUrl': u'http://www.fernsehserien.de/terra-x',
 u'url': u'http://www.fernsehserien.de/terra-x',
 u'visibleUrl': u'www.fernsehserien.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:4V0t4fQZBQMJ:www.wunschliste.de',
 u'content': u'Mediathek zu <b>Terra X</b> / ZDF Expedition D, 1982 - ... 43:00, 18.04.2015. ZDF, 123 \n<b>Phantome der Tiefsee (2): Monsterhaie</b>, 43:00, 18.04.2015. ZDF, 125 Die Macht\xa0...',
 u'title': u'<b>Terra X</b> Mediathek - wunschliste.de',
 u'titleNoFormatting': u'Terra X Mediathek - wunschliste.de',
 u'unescapedUrl': u'http://www.wunschliste.de/serie/terra-x/videos',
 u'url': u'http://www.wunschliste.de/serie/terra-x/videos',
 u'visibleUrl': u'www.wunschliste.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:4V0t4fQZBQMJ:www.wunschliste.de',
 u'content': u'Mediathek zu <b>Terra X</b> / ZDF Expedition D, 1982 - ... 43:00, 18.04.2015. ZDF, 123 \n<b>Phantome der Tiefsee (2): Monsterhaie</b>, 43:00, 18.04.2015. ZDF, 125 Die Macht\xa0...',
 u'title': u'<b>Terra X</b> Mediathek - wunschliste.de',
 u'titleNoFormatting': u'Terra X Mediathek - wunschliste.de',
 u'unescapedUrl': u'http://www.wunschliste.de/serie/terra-x/videos',
 u'url': u'http://www.wunschliste.de/serie/terra-x/videos',
 u'visibleUrl': u'www.wunschliste.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:qkl6FNHYNfUJ:www.wunschliste.de',
 u'content': u'<b>Terra X</b> / ZDF Expedition D, 1982 - : News, Episodenf\xfchrer, TV-Ausstrahlung, ... \n<b>Terra X</b> - Episodenliste ..... 123.123 <b>Phantome der Tiefsee (2): Monsterhaie</b>.',
 u'title': u'<b>Terra X</b> Episodenguide - wunschliste.de',
 u'titleNoFormatting': u'Terra X Episodenguide - wunschliste.de',
 u'unescapedUrl': u'http://www.wunschliste.de/serie/terra-x/episoden',
 u'url': u'http://www.wunschliste.de/serie/terra-x/episoden',
 u'visibleUrl': u'www.wunschliste.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:qkl6FNHYNfUJ:www.wunschliste.de',
 u'content': u'<b>Terra X</b> / ZDF Expedition D, 1982 - : News, Episodenf\xfchrer, TV-Ausstrahlung, ... \n<b>Terra X</b> - Episodenliste ..... 123.123 <b>Phantome der Tiefsee (2): Monsterhaie</b>.',
 u'title': u'<b>Terra X</b> Episodenguide - wunschliste.de',
 u'titleNoFormatting': u'Terra X Episodenguide - wunschliste.de',
 u'unescapedUrl': u'http://www.wunschliste.de/serie/terra-x/episoden',
 u'url': u'http://www.wunschliste.de/serie/terra-x/episoden',
 u'visibleUrl': u'www.wunschliste.de'}


[site:imdb.com "Mord mit Aussicht" "Vatertag"]

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:fpU7DY3jBCsJ:www.imdb.com',
 u'content': u'<b>Vatertag</b> (2008) Poster. Contact the ... <b>Mord mit Aussicht</b>: Season 1, Episode 2. \n<b>Vatertag</b> (14 Jan. .... Discuss <b>Vatertag</b> (2008) on the IMDb message boards \xbb.',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; <b>Vatertag</b> (TV Episode 2008) - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; Vatertag (TV Episode 2008) - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/title/tt1172564/',
 u'url': u'http://www.imdb.com/title/tt1172564/',
 u'visibleUrl': u'www.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:fpU7DY3jBCsJ:www.imdb.com',
 u'content': u'<b>Vatertag</b> (2008) Poster. Contact the ... <b>Mord mit Aussicht</b>: Season 1, Episode 2. \n<b>Vatertag</b> (14 Jan. .... Discuss <b>Vatertag</b> (2008) on the IMDb message boards \xbb.',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; <b>Vatertag</b> (TV Episode 2008) - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; Vatertag (TV Episode 2008) - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/title/tt1172564/',
 u'url': u'http://www.imdb.com/title/tt1172564/',
 u'visibleUrl': u'www.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:xCFVyJzw9UcJ:m.imdb.com',
 u'content': u'Full Cast &amp; Crew: <b>Vatertag</b> (2008). Cast (15). Caroline Peters. \nKriminaloberkommissarin Sophie Haas \xb7 Bjarne M\xe4del. Polizeiobermeister \nDietmar Sch\xe4ffer\xa0...',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; <b>Vatertag</b> (TV Episode 2008) - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; Vatertag (TV Episode 2008) - IMDb',
 u'unescapedUrl': u'http://m.imdb.com/title/tt1172564/fullcredits/cast?ref_=m_ttfc_3',
 u'url': u'http://m.imdb.com/title/tt1172564/fullcredits/cast%3Fref_%3Dm_ttfc_3',
 u'visibleUrl': u'm.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:xCFVyJzw9UcJ:m.imdb.com',
 u'content': u'Full Cast &amp; Crew: <b>Vatertag</b> (2008). Cast (15). Caroline Peters. \nKriminaloberkommissarin Sophie Haas \xb7 Bjarne M\xe4del. Polizeiobermeister \nDietmar Sch\xe4ffer\xa0...',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; <b>Vatertag</b> (TV Episode 2008) - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; Vatertag (TV Episode 2008) - IMDb',
 u'unescapedUrl': u'http://m.imdb.com/title/tt1172564/fullcredits/cast?ref_=m_ttfc_3',
 u'url': u'http://m.imdb.com/title/tt1172564/fullcredits/cast%3Fref_%3Dm_ttfc_3',
 u'visibleUrl': u'm.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:AWgicsK1vPwJ:www.imdb.com',
 u'content': u'<b>Mord mit Aussicht</b> on IMDb: Movies, TV, Celebs, and more... ... Season 1, \nEpisode 2: <b>Vatertag</b>. 14 January 2008. Caroline Peters ... \nKriminaloberkommissarin\xa0...',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; (2008) - Episodes cast - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; (2008) - Episodes cast - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/title/tt1163573/epcast',
 u'url': u'http://www.imdb.com/title/tt1163573/epcast',
 u'visibleUrl': u'www.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:AWgicsK1vPwJ:www.imdb.com',
 u'content': u'<b>Mord mit Aussicht</b> on IMDb: Movies, TV, Celebs, and more... ... Season 1, \nEpisode 2: <b>Vatertag</b>. 14 January 2008. Caroline Peters ... \nKriminaloberkommissarin\xa0...',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; (2008) - Episodes cast - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; (2008) - Episodes cast - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/title/tt1163573/epcast',
 u'url': u'http://www.imdb.com/title/tt1163573/epcast',
 u'visibleUrl': u'www.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:fGG9MSxyW-AJ:www.imdb.com',
 u'content': u'Gabi Weiss, Actress: <b>Mord mit Aussicht</b>. Gabi Weiss is an actress, known for <b>Mord</b> \n<b>mit Aussicht</b> (2008), Die Camper (1997) and Lindenstra\xdfe ... <b>Vatertag</b> (2008) .',
 u'title': u'Gabi Weiss - IMDb',
 u'titleNoFormatting': u'Gabi Weiss - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/name/nm2881956/',
 u'url': u'http://www.imdb.com/name/nm2881956/',
 u'visibleUrl': u'www.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:fGG9MSxyW-AJ:www.imdb.com',
 u'content': u'Gabi Weiss, Actress: <b>Mord mit Aussicht</b>. Gabi Weiss is an actress, known for <b>Mord</b> \n<b>mit Aussicht</b> (2008), Die Camper (1997) and Lindenstra\xdfe ... <b>Vatertag</b> (2008) .',
 u'title': u'Gabi Weiss - IMDb',
 u'titleNoFormatting': u'Gabi Weiss - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/name/nm2881956/',
 u'url': u'http://www.imdb.com/name/nm2881956/',
 u'visibleUrl': u'www.imdb.com'}


[site:thetvdb.com "Mord mit Aussicht" "Vatertag"]


[ "Mord mit Aussicht" "Vatertag"]

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:fpU7DY3jBCsJ:www.imdb.com',
 u'content': u'<b>Vatertag</b> (2008) Poster. Contact the ... <b>Mord mit Aussicht</b>: Season 1, Episode 2. \n<b>Vatertag</b> (14 Jan. .... Discuss <b>Vatertag</b> (2008) on the IMDb message boards \xbb.',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; <b>Vatertag</b> (TV Episode 2008) - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; Vatertag (TV Episode 2008) - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/title/tt1172564/',
 u'url': u'http://www.imdb.com/title/tt1172564/',
 u'visibleUrl': u'www.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:fpU7DY3jBCsJ:www.imdb.com',
 u'content': u'<b>Vatertag</b> (2008) Poster. Contact the ... <b>Mord mit Aussicht</b>: Season 1, Episode 2. \n<b>Vatertag</b> (14 Jan. .... Discuss <b>Vatertag</b> (2008) on the IMDb message boards \xbb.',
 u'title': u'&quot;<b>Mord mit Aussicht</b>&quot; <b>Vatertag</b> (TV Episode 2008) - IMDb',
 u'titleNoFormatting': u'&quot;Mord mit Aussicht&quot; Vatertag (TV Episode 2008) - IMDb',
 u'unescapedUrl': u'http://www.imdb.com/title/tt1172564/',
 u'url': u'http://www.imdb.com/title/tt1172564/',
 u'visibleUrl': u'www.imdb.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:VtkWGz3DKtMJ:www.dailymotion.com',
 u'content': u'3. Okt. 2015 <b>...</b> <b>Mord mit Aussicht</b> Staffel 1. Folge 2 - Ausgerechnet am feuchtfr\xf6hlichen <b>Vatertag</b> \nwird eine Leiche in Hengasch entdeckt - und es sieht erstmal\xa0...',
 u'title': u'<b>Mord mit Aussicht</b> Folge 2 &quot;<b>Vatertag</b>&quot; - Dailymotion-Video',
 u'titleNoFormatting': u'Mord mit Aussicht Folge 2 &quot;Vatertag&quot; - Dailymotion-Video',
 u'unescapedUrl': u'http://www.dailymotion.com/video/x38gy1t',
 u'url': u'http://www.dailymotion.com/video/x38gy1t',
 u'visibleUrl': u'www.dailymotion.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:VtkWGz3DKtMJ:www.dailymotion.com',
 u'content': u'3. Okt. 2015 <b>...</b> <b>Mord mit Aussicht</b> Staffel 1. Folge 2 - Ausgerechnet am feuchtfr\xf6hlichen <b>Vatertag</b> \nwird eine Leiche in Hengasch entdeckt - und es sieht erstmal\xa0...',
 u'title': u'<b>Mord mit Aussicht</b> Folge 2 &quot;<b>Vatertag</b>&quot; - Dailymotion-Video',
 u'titleNoFormatting': u'Mord mit Aussicht Folge 2 &quot;Vatertag&quot; - Dailymotion-Video',
 u'unescapedUrl': u'http://www.dailymotion.com/video/x38gy1t',
 u'url': u'http://www.dailymotion.com/video/x38gy1t',
 u'visibleUrl': u'www.dailymotion.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:uB0KWa0PaL4J:www.dailymotion.com',
 u'content': u'18. Apr. 2015 <b>...</b> Sieh dir das Video &quot;<b>Vatertag</b> 2014&quot; an, das Motorsportjunky auf Dailymotion \nhochgeladen hat. ... <b>Mord mit Aussicht</b> Folge 2 &quot;<b>Vatertag</b>&quot;.',
 u'title': u'<b>Vatertag</b> 2014 - Dailymotion-Video',
 u'titleNoFormatting': u'Vatertag 2014 - Dailymotion-Video',
 u'unescapedUrl': u'http://www.dailymotion.com/video/x2n3hxy',
 u'url': u'http://www.dailymotion.com/video/x2n3hxy',
 u'visibleUrl': u'www.dailymotion.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'http://www.google.com/search?q=cache:uB0KWa0PaL4J:www.dailymotion.com',
 u'content': u'18. Apr. 2015 <b>...</b> Sieh dir das Video &quot;<b>Vatertag</b> 2014&quot; an, das Motorsportjunky auf Dailymotion \nhochgeladen hat. ... <b>Mord mit Aussicht</b> Folge 2 &quot;<b>Vatertag</b>&quot;.',
 u'title': u'<b>Vatertag</b> 2014 - Dailymotion-Video',
 u'titleNoFormatting': u'Vatertag 2014 - Dailymotion-Video',
 u'unescapedUrl': u'http://www.dailymotion.com/video/x2n3hxy',
 u'url': u'http://www.dailymotion.com/video/x2n3hxy',
 u'visibleUrl': u'www.dailymotion.com'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'',
 u'content': u'<b>Mord mit Aussicht</b> (2). <b>Vatertag</b>. Samstag, 25. Juli 2015, 22:35 bis 23:25 Uhr. \nAusgerechnet am feuchtfr\xf6hlichen <b>Vatertag</b> wird eine Leiche in Hengasch \nentdeckt.',
 u'title': u'<b>Vatertag</b> | NDR.de - Fernsehen - TV-Programm - import',
 u'titleNoFormatting': u'Vatertag | NDR.de - Fernsehen - TV-Programm - import',
 u'unescapedUrl': u'http://www.ndr.de/fernsehen/epg/import/Vatertag,sendung80694.html',
 u'url': u'http://www.ndr.de/fernsehen/epg/import/Vatertag,sendung80694.html',
 u'visibleUrl': u'www.ndr.de'}

{u'GsearchResultClass': u'GwebSearch',
 u'cacheUrl': u'',
 u'content': u'<b>Mord mit Aussicht</b> (2). <b>Vatertag</b>. Samstag, 25. Juli 2015, 22:35 bis 23:25 Uhr. \nAusgerechnet am feuchtfr\xf6hlichen <b>Vatertag</b> wird eine Leiche in Hengasch \nentdeckt.',
 u'title': u'<b>Vatertag</b> | NDR.de - Fernsehen - TV-Programm - import',
 u'titleNoFormatting': u'Vatertag | NDR.de - Fernsehen - TV-Programm - import',
 u'unescapedUrl': u'http://www.ndr.de/fernsehen/epg/import/Vatertag,sendung80694.html',
 u'url': u'http://www.ndr.de/fernsehen/epg/import/Vatertag,sendung80694.html',
 u'visibleUrl': u'www.ndr.de'}

                         print episode.seasonid, episode.SeasonNumber, episode.EpisodeNumber, episode.EpisodeName
                        print 'fuzz ratio=', \
                            fuzz.ratio(search, name),\
                            fuzz.partial_ratio(search, name),\
                            fuzz.token_sort_ratio(search, name),\
                            fuzz.token_set_ratio(search, name)


                        if episode.EpisodeName == self.data['subtitle']:
                            print 'Found!'


'''