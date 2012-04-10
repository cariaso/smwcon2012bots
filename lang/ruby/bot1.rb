#!/usr/bin/env ruby
#########################################
#
# Read more at
#
# http://github.com/jpatokal/mediawiki-gateway
#
#########################################
#
# comment out 'private' in mediawiki-gateway/lib/media_wiki/gateway.rb line 563
# since the standard version makes make_api_request() inaccessible
#
# git clone git://github.com/jpatokal/mediawiki-gateway.git
#########################################

$LOAD_PATH << 'mediawiki-gateway/lib'

require 'media_wiki'

# you may also need 
# "sudo gem install rest-client"
# "sudo gem install active_support"












#############################################################
# Settings
#############################################################

api_url = 'http://sandbox.semantic-mediawiki.org/api.php'
username='Cariaso'
password='correct horse battery staple'






#############################################################
# Read Category Titles 
#############################################################


def DemoReadCategoryTitles1(mw)

    # surprisingly difficult, no ruby api for this
    # https://github.com/jpatokal/mediawiki-gateway/issues/9

    puts "---\nBegin DemoReadCategoryTitles1"

    form_data = { 'action' => 'query', 
		  'list' => 'categorymembers',
                  'cmtitle'=>'Category:City'
                }
    xml, dummy = mw.make_api_request(form_data)
    results = xml.elements["query/categorymembers"]
    
    if results != nil
      results.each do |p| 
        puts p.attributes["title"]
      end
    end

end






#############################################################
# Read Text
#############################################################


def DemoReadPageText(mw)

    puts "---\nBegin DemoReadPageText\n"

    pagename = 'Berlin'
    pagetext = mw.get(pagename)
    puts "\n================BEGIN==="
    puts "From Page %s" % pagename
    puts pagetext
    puts "\n================END==="




    cities = ['Warsaw', 'San Diego']
    cities.each {|city| 
        pagetext = mw.get(city)
        puts "\n================BEGIN==="
        puts "From Page %s" % city
        puts pagetext
        puts "\n================END==="
    }


end



#############################################################
# Write a Page
#############################################################

    
def DemoWritePageText(mw)

    puts "---\nBegin DemoWritePageText\n"

    pagename = "JustASandbox"
    now = Time.new.inspect
    newtext = "This is from ruby at " + now + "\n\n"
    mw.edit(pagename, newtext)


end

#############################################################
# Append to a Page
#############################################################


def DemoAppendPageText(mw)

    puts "---\nBegin DemoAppendPageText\n"

    pagename = "JustASandbox"
    now = Time.new.inspect
    extratext = "This is from ruby at " + now + "\n\n"


    oldtext = mw.get(pagename)
    newtext = oldtext + "\n" + extratext
    mw.edit(pagename, newtext)


end



#############################################################
# Semantic ask
#############################################################

require 'pp'

def DemoSemanticAsk(mw)


    form_data = { 'action'     => 'askargs',
                  'conditions' => 'Category:City | located in::Germany',
                  'printouts'  => 'area|population',
                  'parameters' =>'|sort=Modification date|order=desc',
                }
    xml, dummy = mw.make_api_request(form_data)
    results = xml.elements["query/results"]
    
    
    if results != nil
      results.each do |p| 
        name       = p.attributes["fulltext"]
        population = p.elements["printouts/population/value"].text
        area       = p.elements["printouts/area/value"].attributes["fulltext"]

        print  name, " \t ", population, " \t ", area, "\n"
      end
    end


    # Note. There is a method for semantic_query but it doesn't seem to work yet
    # http://rubydoc.info/gems/mediawiki-gateway/0.4.4/MediaWiki/Gateway:semantic_query

end








#############################################################
# main
#############################################################

mw = MediaWiki::Gateway.new(api_url)


#DemoReadCategoryTitles1(mw)
#DemoReadPageText(mw)
DemoSemanticAsk(mw)

mw.login(username, password)

#DemoWritePageText(mw)
#DemoAppendPageText(mw)

