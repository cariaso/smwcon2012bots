#!/usr/bin/env python

import sys
import os
import urllib2
import re

import wikitools
# http://code.google.com/p/python-wikitools/



def main():

    api_url = 'http://semantic-mediawiki.org/w/api.php'
    params = { 'action' : 'askargs',
               'conditions' : 'Category:SMW_site',
               'printouts'  : 'Homepage|APIURL',
               'parameters' : '|output=table',

               # printouts don't work with these parameters below
               #parameters =>'|sort=Modification date|order=desc',
               # blank or missing cause a server side error
               }

    mw = wikitools.wiki.Wiki(api_url)

    req = wikitools.wiki.api.APIRequest(mw, params)
    resp = req.query()

    results = resp['query']['results']
    for item in results:
        if item.startswith('File:'): continue
        try:
            homepage = results[item]['printouts']['Homepage'][0]
        except:
            homepage = ''

        try:
            apiurl = results[item]['printouts']['APIURL'][0]
        except:
            apiurl = ''

        site_api_url = guess_api_url(apiurl, homepage)




        # Check for gzip compression on a json response

        if site_api_url:
            address = site_api_url+'?action=smwinfo&format=json'
            request = urllib2.Request(address)
        else:
            request = None

        
        try:
            response = urllib2.urlopen(request)
            code = 200
            encoding = response.info().getheader('content-encoding')
            text = response.read()
        except urllib2.HTTPError as e:
            code = e.code
            encoding = e.info().getheader('content-encoding')
            text = e.read()
        except Exception as e:
            code = encoding = text = ''

        status = ''
        if text.startswith('{') and text.endswith('}'):
            status = 'OK'

        print status,'\t',code,'\t',encoding,'\t',item,'           \t',site_api_url;



def guess_api_url(apival, homepage=None):
    if apival: return apival
    if homepage:
        site_api_url = homepage + '/api.php';
        site_api_url = re.sub(r'//api', r'/api', site_api_url)
        site_api_url = re.sub(r'/wiki/.*api.php', r'/wiki/api.php', site_api_url)
        site_api_url = re.sub(r'/index.php.*', r'/api.php', site_api_url)
        return site_api_url
    return None



if __name__ == '__main__':
    main()

