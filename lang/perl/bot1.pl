#!/bin/env perl

use strict;
use warnings;
use Data::Dumper;


use MediaWiki::API;

#########################################
#
# Read more at
#
# http://search.cpan.org/~exobuzz/MediaWiki-API-0.37/lib/MediaWiki/API.pm
#
#########################################













#############################################################
# Settings
#############################################################

my $api_url = 'http://sandbox.semantic-mediawiki.org/w/api.php';
my $username='Cariaso';
my $password='correct horse battery staple';





#############################################################
# Read Category Titles : Small
#############################################################




sub DemoReadCategoryTitles1 {
    my ($mw) = @_;

    print "---\nBegin DemoReadCategoryTitles1\n";

    my $ref = $mw->list ( { action => 'query',
			    list => 'categorymembers',
			    cmtitle => 'Category:City',
			    cmnamespace => 0,
			    cmlimit=>'100' } )
	|| die $mw->{error}->{code} . ': ' . $mw->{error}->{details};


    foreach my $city (@$ref) {
	print $city->{title},"\n";
    }
    
}







#############################################################
# Read Category Titles : Large
#############################################################

# This version is needed to correctly process all pages in large
# categories
 

sub print_articles {
    my ($ref) = @_;
    foreach (@$ref) {
	print "$_->{title}\n";
    }
}


sub DemoReadCategoryTitles2 {
    my ($mw) = @_;

    print "---\nBegin DemoReadCategoryTitles2\n";

    $mw->list ( { action => 'query',
		  list => 'categorymembers',
		  cmtitle => 'Category:City',
		  cmnamespace => 0,
		  cmlimit=>'100' },
		{ max => 4, hook => \&print_articles } )
	|| die $mw->{error}->{code} . ': ' . $mw->{error}->{details};
    
}





#############################################################
# Read Text
#############################################################


sub DemoReadPageText {
    my ($mw) = @_;

    print "---\nBegin DemoReadPageText\n";

    my $pagename = 'Berlin';
    my $page     = $mw->get_page( { title => $pagename } );
    my $pagetext = $page->{'*'};
    print "\n================BEGIN===\n";
    print "From Page $pagename\n";
    print $pagetext;
    print "\n================END===\n";





    foreach my $city ('Warsaw','San Diego') {

	my $page = $mw->get_page( { title => $city } );
	my $pagetext = $page->{'*'};

	print "\n================BEGIN===\n";
	print "From Page $city\n";
	print $pagetext;
	print "\n================END===\n";
    }
}






#############################################################
# Write a Page
#############################################################



sub DemoWritePageText {
    my ($mw) = @_;

    print "---\nBegin DemoWritePageText\n";

    my $pagename = "JustASandbox";
    my $now = scalar(localtime);
    my $newtext = "This is from perl at $now\n\n";

    $mw->edit( {
	action => 'edit',
	title => $pagename,
	text => $newtext } )
	|| die $mw->{error}->{code} . ': ' . $mw->{error}->{details};
}




#############################################################
# Append to a Page
#############################################################



# This example is for adding some text to an existing page (if the
# page doesn't exist nothing will happen). Note that the timestamp for
# the revision we are changing is saved. This allows us to avoid edit
# conflicts. The value is passed back to the edit function, and if
# someone had edited the page in the meantime, an error will be
# returned.

sub DemoAppendPageText {
    my ($mw) = @_;

    print "---\nBegin DemoAppendPageText\n";

    my $pagename = "JustASandbox";
    my $now = scalar(localtime);
    my $ref = $mw->get_page( { title => $pagename } );

    my $oldtext = $ref->{'*'};
    my $newtext = "$oldtext\nAdditional text from perl at $now";

    unless ( $ref->{missing} ) {
	my $timestamp = $ref->{timestamp};
	$mw->edit( {
	    action => 'edit',
	    title => $pagename,
	    basetimestamp => $timestamp, # to avoid edit conflicts
	    text => $newtext } )
	    || die $mw->{error}->{code} . ': ' . $mw->{error}->{details};
    }
    
}





#############################################################
# Semantic ask
#############################################################

sub DemoSemanticAsk {
    my ($mw) = @_;

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


    foreach my $name (keys %{$response->{query}->{results}}) {
        print "  $name\n";
    }
}




#############################################################
# main
#############################################################

my $mw = MediaWiki::API->new();
$mw->{config}->{api_url} = $api_url;

DemoReadCategoryTitles1($mw);
DemoReadCategoryTitles2($mw);
DemoReadPageText($mw);

my $res = $mw->login( { lgname => $username, 
                        lgpassword => $password 
                      } ) 
    || die $mw->{error}->{code} . ': ' . $mw->{error}->{details};

DemoWritePageText($mw);
DemoAppendPageText($mw);
DemoSemanticAsk($mw);






