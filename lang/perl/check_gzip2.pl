#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;


use MediaWiki::API;
# http://search.cpan.org/~exobuzz/MediaWiki-API-0.37/lib/MediaWiki/API.pm



my @titles = ();

sub remember_titles {
    my ($ref) = @_;
    foreach (@$ref) {
	push @titles, $_->{title};
    }
}


my $mw_api_url = 'http://semantic-mediawiki.org/w/api.php';

my $mw = MediaWiki::API->new();
$mw->{config}->{api_url} = $mw_api_url;

my $ref = $mw->list ( { action => 'query',
			list => 'categorymembers',
			cmtitle => 'Category:Wiki_of_the_Month',
			cmnamespace => 0,
			cmlimit=>'100' },
		      { max => 4, hook => \&remember_titles } )
    || warn $mw->{error}->{code} . ': ' . $mw->{error}->{details};


my $regex = qr/
        (                   # start of bracket 1
        {                   # match an opening curly
            (?:
                [^{}]++     # one or more non angle brackets, non backtracking
                  |
                (?1)        # recurse to bracket 1
            )*
        }                   # match a closing curly
        )                   # end of bracket 1
        /x;


my $ua = LWP::UserAgent->new;
my $can_accept = HTTP::Message::decodable;
my $mw_checker = MediaWiki::API->new();

foreach my $title (@titles) {
    
    my $page     = $mw->get_page( { title => $title } );
    my $pagetext = $page->{'*'};
    my @templates = $pagetext =~ m/$regex/g;
    my @url = grep /^\s*\|\s*url\s*=/i, split(/\n/, ($templates[0]||''));
    my ($address) = ($url[0]||'') =~ /(http[^\s\|\}]+)/;
    #next unless $address;
    #next unless $address =~ /index.php/;


    #print Dumper \@infoboxes, \@url, $address;
    #print "$title\t::\t$address\n";

    my $response = $ua->get($address, 
			    'Accept-Encoding' => $can_accept);
    my $encoding = $response->{_headers}->{'content-encoding'};
    $encoding ||= '';
    $address ||= '';
    print "$encoding\t$title\t::\t$address\n";
    next;
    #print Dumper $response->{_headers};
    #print $response->decoded_content;

    my $api_url = $address;
    $api_url =~ s/index.php.*/api.php/;

    $mw_checker->{config}->{api_url} = $api_url;


    eval {
	my $ref = $mw_checker->api ( { 
	    action => 'query',
	    prop=>'info',
	    titles=>'Main Page',
				     },
	    );
	
	if (exists($ref->{query})) {
	    print Dumper $ref;
	}
    };
    if ($@) {
	print "Unable to work wth $title\n";
    }
}

