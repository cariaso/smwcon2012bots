#!/bin/env python

import sys
sys.path.append('pywikipedia')
sys.path.append('pywikipedia/userinterfaces')



import query



userquery = '''
{{#ask: [[Category:City]] [[located in::Germany]]
| ?population
| ?Area
}}
'''

params = {
    'action':'ask',
    'query' :userquery,
    }
                                                                                                                                                          
response = query.GetData(params)
allitems = response['query']['results']
for item in allitems:
    print item

