#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper;
use MediaWiki::Bot;


my $bot = MediaWiki::Bot->new({
    host        => $ENV{BOTHOST} || 'localhost',
    login_data  => {
        username => $ENV{BOTUSER} || "WikiAdmin",
        password => $ENV{BOTPASS} || "abadpassword"
    },
    useragent   => 'MyLoaderBot (me@example.com)',
    protocol    => 'http',
    path        => '/',
    assert      => 'bot',

    }) or die("Bot unable to connect to the wiki");





my $car_template_text = <<TEMPLATE1;
<includeonly>
<div style="float:right; margin:1em; width: 25em; text-align: left; font-size: 90%; border:thin solid;">
<table>
    <tr><td>MPG</td><td>[[MPG::{{{MPG|}}}]]</td></tr>
    <tr><td>Cylinders</td><td>[[Cylinders::{{{Cylinders|}}}]]</td></tr>
    <tr><td>CC</td><td>[[CC::{{{CC|}}}]]</td></tr>
    <tr><td>Horsepower</td><td>[[Horsepower::{{{Horsepower|}}}]]</td></tr>
    <tr><td>Weight</td><td>[[Weight::{{{Weight|}}}]]</td></tr>
    <tr><td>ZeroTo60</td><td>[[ZeroTo60::{{{ZeroTo60|}}}]]</td></tr>
    <tr><td>Year</td><td>[[Year::{{{Year|}}}]]</td></tr>
</table>
</div>
</includeonly><noinclude>
This is a navigation bar for Cars
*''MPG''
*''Cylinders''
*''CC'' Displacement in cubic centimeters
*''Horsepower'' Hasta la caballo revelucion!
*''Weight'' in pounds
*''ZeroTo60'' in seconds
*''Year''
</noinclude>
TEMPLATE1

$bot->edit({
    page    => 'Template:Car',
    summary => 'Provide a template',
    text    => $car_template_text,
	       });



use FileHandle;




my $localfn = 'data/cars.csv';
my $cartext;
if (-e $localfn) {
    open(my $fh, "<", $localfn) 
	or die "cannot open < $localfn: $!";
    local $/ = undef;
    $cartext = <$fh>;
} else {
    # From a URL
    my $url = "https://raw.github.com/0xdata/h2o/master/smalldata/cars.csv";
    $cartext = `wget -O - $url 2> /dev/null`
}
die("Unable to load the car data") unless $cartext;



my @carlines = split(/\n/,$cartext);
my $topline = shift @carlines;

my $uniquename = 'Car200';
foreach my $carline (@carlines) {
    my @fields = split(/,/, $carline);
    #my $title = $fields[0];
    my $title = $uniquename++;

    my $pagetext = "{{Car
|MPG=$fields[1]
|Cylinders=$fields[2]
|CC=$fields[3]
|Horsepower=$fields[4]
|Weight=$fields[5]
|ZeroTo60=$fields[6]
|Year=$fields[7]
}}";
    #print Dumper $title, $pagetext;

    $bot->edit({
	page    => $title,
	text    => $pagetext,
	summary => 'Adding a new car',
	       });
    print "Loaded $title\n";
}






