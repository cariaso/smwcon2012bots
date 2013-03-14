#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
use MediaWiki::Bot;

# From a local file
use File::Slurp;
my $cartext = read_file('data/cars.csv');

# From a URL
#my $url = "http://raw.github.com/0xdata/h2o/master/smalldata/cars.csv";
#use LWP::Simple;
#my $cartext = get($url) or die("Unable to get the csv file from github");
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



