#!/bin/env python

# Pywikipedia really wants settings in the filesystem. It depends on
# particular paths and filenames all of which make simple bots very
# complicated. More complicated bots eventually reap the rewards, but
# this minimal example is scary.
#


# svn co http://svn.wikimedia.org/svnroot/pywikipedia/trunk/pywikipedia pywikipedia
import sys
sys.path.append('pywikipedia') 
sys.path.append('pywikipedia/userinterfaces') 



import os

import tempfile
import atexit
import shutil

siteparams = {'host':'sandbox.semantic-mediawiki.org',
              'apipath':'/w/api.php'}

sitename = 'mysite'

def cleanup(dir):
    def f():
        shutil.rmtree(dir) 
    return f


familydir = tempfile.mkdtemp()
atexit.register(cleanup(familydir))

os.environ["PYWIKIBOT_DIR"] = familydir

userconfigfn = '%s/user-config.py' % familydir
if True:
    fh = file(userconfigfn,'w')
    userconftxt = """# -*- coding: utf-8  -*-
family = '%(myname)s'
mylang = 'en'
usernames['%(myname)s']['en'] = u'mybot'
console_encoding = 'utf-8'
""" % {'myname':sitename}
    fh.write(userconftxt)
    fh.close()

    os.mkdir('%s/families' % familydir)

    fh = file('%s/families/%s_family.py' % (familydir, sitename),'w')
    message = """# -*- coding: utf-8  -*-
import family
class Family(family.Family):
    def __init__(self):
       family.Family.__init__(self)
       self.name = 'mywiki'
       self.langs = {
           'en': '%(host)s',
          }
       self.namespaces[102] = { 'en': 'Property' }

    def version(self, code):
        return "1.17"

    def apipath(self, code):
       return '%(apipath)s'

""" % siteparams
    fh.write(message)
    fh.close()


import query


if True:
    userquery = '''
{{#ask: [[Category:City]] [[located in::Germany]] 
| ?population 
| ?Area
}}
'''

    params = {
        'action':'ask',
        'query'     :userquery,
        }                                                                                                                                                 
                                                                                                                                                          
    response = query.GetData(params)
    allitems = response['query']['results']
    for item in allitems:
        print item

