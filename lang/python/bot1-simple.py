#!/bin/env python


# svn checkout http://python-wikitools.googlecode.com/svn/trunk/wikitools/ python-wikitools-read-only
import sys
sys.path.append('python-wikitools-read-only')









userquery = '''
{{#ask: [[Category:City]] [[located in::Germany]] 
| ?population 
| ?Area
}}
'''

import wiki
site = wiki.Wiki("http://www.semantic-mediawiki.org/w/api.php")
params = {'action':'ask',
          'query':userquery
          }
req = wiki.api.APIRequest(site, params)
resp = req.query()

allitems = resp['query']['results']
for item in allitems:
    print item

