#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;

use MediaWiki::API;
# http://search.cpan.org/~exobuzz/MediaWiki-API-0.37/lib/MediaWiki/API.pm

my $mw_api_url = 'http://semantic-mediawiki.org/w/api.php';
my $params = {
    action     => 'askargs',
    conditions => 'Category:SMW_site',
    printouts  => 'Homepage|APIURL',
    parameters =>'|format=table',
    
    # printouts don't work with these parameters below
    #parameters =>'|sort=Modification date|order=desc',
    # blank or missing cause a server side error
};

my $mw = MediaWiki::API->new();
$mw->{config}->{api_url} = $mw_api_url;

my $response = $mw->api($params)
    || warn $mw->{error}->{code} . ': ' . $mw->{error}->{details};

my $results = $response->{query}->{results};



my $ua = LWP::UserAgent->new;
my $can_accept = HTTP::Message::decodable;

foreach my $name (sort keys %$results) {
    next if $name =~ /^File:/;
    my $homepage = $results->{$name}->{'printouts'}->{'Homepage'}[0] || '';
    my $site_api_url = $results->{$name}->{'printouts'}->{'APIURL'}[0] || '';



    # if no APIURL was provided, make a decent guess
    if (!$site_api_url) {
	$site_api_url = $homepage .'/api.php';
	$site_api_url =~ s!//api!/api!;
	$site_api_url =~ s!/wiki/.*api.php!/wiki/api.php!;
	$site_api_url =~ s!/index.php.*!/api.php!;
	
    }


    # Check for gzip compression on a json response
    my $address = "$site_api_url?action=smwinfo&format=json";
    my $response = $ua->get($address, 
			    'Accept-Encoding' => $can_accept);
    my $code = $response->{_rc};
    my $text = $response->decoded_content;
    my $status = '';
    if ($text =~ /^\{.*\}$/) {
	$status = 'OK';
    }
    #print $text;
    #print Dumper $response;
    my $encoding = $response->{_headers}->{'content-encoding'} || '';

    print "$status\t$code\t$encoding\t$name           \t$site_api_url\n";
}
