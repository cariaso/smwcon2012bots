#!/bin/env python


# svn checkout http://python-wikitools.googlecode.com/svn/trunk/wikitools/ python-wikitools-read-only
import sys
sys.path.append('python-wikitools-read-only')


#########################################
#
# Read more at
#
# http://code.google.com/p/python-wikitools/
#
#########################################


import wiki
import category
import page






#############################################################
# Settings
#############################################################

api_url = 'http://sandbox.semantic-mediawiki.org/w/api.php'
username='Cariaso'
password='correct horse battery staple'






#############################################################
# Read Category Titles 
#############################################################


def DemoReadCategoryTitles1(mw):

    print "---\nBegin DemoReadCategoryTitles1"

    cities = category.Category(mw, "City")
    for article in cities.getAllMembersGen(namespaces=[0]):
        print article.title









#############################################################
# Read Text
#############################################################


def DemoReadPageText(mw):

    print "---\nBegin DemoReadPageText\n"

    pagename = 'Berlin'
    pagetext = page.Page(mw, pagename).getWikiText()
    print "\n================BEGIN==="
    print "From Page %s" % pagename
    print pagetext
    print "\n================END==="





    for city in ('Warsaw','San Diego'):

        pagetext = page.Page(mw, city).getWikiText()
        print "\n================BEGIN==="
        print "From Page %s" % pagename
        print pagetext
        print "\n================END==="


#############################################################
# Write a Page
#############################################################

    
def DemoWritePageText(mw):

    print "---\nBegin DemoWritePageText\n";

    pagename = "JustASandbox";
    from datetime import datetime
    now = datetime.now()
    newtext = "This is from python at %s\n\n" % now


    article = page.Page(mw, pagename)
    article.edit(newtext)



#############################################################
# Append to a Page
#############################################################


def DemoAppendPageText(mw):

    print "---\nBegin DemoWritePageText\n";

    pagename = "JustASandbox";
    from datetime import datetime
    now = datetime.now()
    extratext = " This is from python at %s\n\n" % now


    article = page.Page(mw, pagename)
    article.edit(appendtext=extratext)






#############################################################
# Semantic ask
#############################################################

def DemoSemanticAsk(mw):


    userquery = '''
{{#ask: [[Category:City]] [[located in::Germany]] 
| ?population 
| ?Area
}}
'''


    params = {'action':'ask',
              'query':userquery
              }
    req = wiki.api.APIRequest(mw, params)
    resp = req.query()

    allitems = resp['query']['results']
    for item in allitems:
        print item



#############################################################
# main
#############################################################


if __name__ == '__main__':
    mw = wiki.Wiki(api_url)

    DemoReadCategoryTitles1(mw)
    DemoReadPageText(mw)

    mw.login(username, password)
    DemoWritePageText(mw)
    DemoAppendPageText(mw)

    DemoSemanticAsk(mw)

