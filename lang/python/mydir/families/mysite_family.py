# -*- coding: utf-8  -*-
import family
class Family(family.Family):
    def __init__(self):
       family.Family.__init__(self)
       self.name = 'mywiki'
       self.langs = {
           'en': 'www.semantic-mediawiki.org',
          }
       self.namespaces[102] = { 'en': 'Property' }

    def version(self, code):
        return "1.17"

    def apipath(self, code):
       return '/w/api.php'

