#!/usr/bin/env python


# svn checkout http://python-wikitools.googlecode.com/svn/trunk/wikitools/
import sys
sys.path.append('wikitools')


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

#api_url = 'http://www.semantic-mediawiki.org/w/api.php'
# the above is to remind you about /w/ and similar


api_url = 'http://sandbox.semantic-mediawiki.org/api.php'
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

    params = {
              'action'     : 'askargs',
              'conditions' : 'Category:City | located in::Germany',
              'printouts'  : 'area|population',
              'parameters' :'|sort=Modification date|order=desc',
              }
    req = wiki.api.APIRequest(mw, params)
    resp = req.query()

    allitems = resp['query']['results']

    for item in allitems:
        print item, allitems[item]['printouts']['population'][0], allitems[item]['printouts']['area'][0]['fulltext']




#############################################################
# main
#############################################################


if __name__ == '__main__':
    mw = wiki.Wiki(api_url)
    mw.login(username, password)

    DemoReadCategoryTitles1(mw)
    DemoReadPageText(mw)

    DemoSemanticAsk(mw)

    DemoWritePageText(mw)
    DemoAppendPageText(mw)


