# need to remove the 'private' from mediawiki-gateway/lib/media_wiki/gateway.rb

# git clone git://github.com/jpatokal/mediawiki-gateway.git
$LOAD_PATH << 'mediawiki-gateway/lib'

require 'media_wiki'


mw = MediaWiki::Gateway.new("http://www.semantic-mediawiki.org/w/api.php")
@userquery = "
{{#ask: [[Category:City]] [[located in::Germany]] 
| ?population 
| ?Area
}}
"


form_data = { 'action' => 'ask', 'query' => @userquery }
xml, dummy = mw.make_api_request(form_data)
results = xml.elements["query/results"]


if results != nil
  results.each do |p| # iterate over the results and grab the full text for each page
    puts p.attributes["fulltext"]
  end
end
