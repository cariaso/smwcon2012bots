#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
use MediaWiki::Bot;

my $localfn = 'data/cars.csv';
my $cartext;
if (-e $localfn) {
    my $fh = open($localfn);
    $cartext = do {local (@ARGV,$/) = $file; <>};
} else {
    # From a URL
    my $url = "http://raw.github.com/0xdata/h2o/master/smalldata/cars.csv";
    #use LWP::Simple;
    #$cartext = get($url) or die("Unable to get the csv file from github");
    $cartext = system("wget -O - $url 2> /dev/null");
}
die("Unable to load the car data") unless $cartext;



my @carlines = split(/\n/,$cartext);
my $topline = shift @carlines;






my $bot = MediaWiki::Bot->new({
    host        => 'localhost',
    login_data  => {
        username => "WikiAdmin",
        password => "abadpassword"
    }}) or die("Bot unable to connect to the wiki");





foreach my $carline (@carlines) {
    my @fields = split(/,/, $carline);
    my $title = $fields[0];

    my $pagetext = "{{Car
|MPG=$fields[1]
|Cylinders=$fields[2]
|CC=$fields[3]
|Horsepower=$fields[4]
|Weight=$fields[5]
|ZeroTo60=$fields[6]
|Year=$fields[7]
}}";
    print Dumper $title, $pagetext;

    $bot->edit({
	page    => $title,
	text    => $pagetext,
	summary => 'Adding a new car',
	       });
}



