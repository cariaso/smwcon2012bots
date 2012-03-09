#!/bin/env perl

use strict;
use warnings;
use Data::Dumper;

use MediaWiki::API;

my $mw = MediaWiki::API->new();
$mw->{config}->{api_url} = 'http://www.semantic-mediawiki.org/w/api.php';


my $query = "
{{#ask: [[Category:City]] [[located in::Germany]] 
| ?population 
| ?Area
}}
";

my $response = $mw->api( {
    action => 'ask',
    query => $query,
    })
       || die $mw->{error}->{code} . ': ' . $mw->{error}->{details};


print Dumper $response;

foreach my $name (keys %{$response->{query}->{results}}) {
    print "  $name\n";
}


