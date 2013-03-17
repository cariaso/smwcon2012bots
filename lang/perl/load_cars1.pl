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
    <tr><td>Name</td><td>[[Name::{{{Name|}}}]]</td></tr>
    <tr><td>MPG</td><td>[[MPG::{{{MPG|}}}]]</td></tr>
    <tr><td>Cylinders</td><td>[[Cylinders::{{{Cylinders|}}}]]</td></tr>
    <tr><td>CC</td><td>[[CC::{{{CC|}}}]]</td></tr>
    <tr><td>Horsepower</td><td>[[Horsepower::{{{Horsepower|}}}]]</td></tr>
    <tr><td>Weight</td><td>[[Weight::{{{Weight|}}}]]</td></tr>
    <tr><td>ZeroTo60</td><td>[[ZeroTo60::{{{ZeroTo60|}}}]]</td></tr>
    <tr><td>Year</td><td>[[Year::{{{Year|}}}]]</td></tr>
</table>
</div>[[Category:Car]]
</includeonly><noinclude>
This is a navigation bar for Cars
*''Name''
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















foreach my $field (
    'MPG',
    'Cylinders',
    'CC',
    'Horsepower',
    'Weight',
    'ZeroTo60',
    'Year',
    ) {

    my $property_text = "[[has type::Number]]";

    $bot->edit({
	page    => "Property:$field",
	summary => 'Make a property',
	text    => $property_text,
	       });
    print "made property $field\n";


    my $filter_text = "This filter covers the property [[Covers property::$field]].";

    $bot->edit({
	page    => "Filter:$field",
	summary => 'Make a filter',
	text    => $filter_text,
	       });
    print "made filter $field\n";
}







my $car_category_text = <<PAGE2;
It has the default form [[Has default form::Car]].

This category uses the filters:
*[[Has filter::Filter:Name]]
*[[Has filter::Filter:MPG]]
*[[Has filter::Filter:Cylinders]]
*[[Has filter::Filter:CC]]
*[[Has filter::Filter:Horsepower]]
*[[Has filter::Filter:Weight]]
*[[Has filter::Filter:ZeroTo60]]
*[[Has filter::Filter:Year]]
PAGE2

$bot->edit({
    page    => 'Category:Car',
    summary => 'Associate the form',
    text    => $car_category_text,
	       });







my $car_form_text = <<PAGE3;
<noinclude>
This is the "Car" form.

To create a page with this form, enter the page name below;
if a page with that name already exists, you will be sent to a form to edit that page.


{{#forminput:form=Car}}

</noinclude><includeonly>
<div id="wikiPreview" style="display: none; padding-bottom: 25px; margin-bottom: 25px; border-bottom: 1px solid #AAAAAA;"></div>
{{{for template|Car}}}

{| class="formtable"
! Name:
| {{{field|Name}}}
|-
! MPG:
| {{{field|MPG}}}
|-
! Cylinders:
| {{{field|Cylinders}}}
|-
! CC:
| {{{field|CC}}}
|-
! Horsepower:
| {{{field|Horsepower}}}
|-
! Weight:
| {{{field|Weight}}}
|-
! ZeroTo60:
| {{{field|ZeroTo60}}}
|-
! Year:
| {{{field|Year}}}
|}
{{{end template}}}

Here you can edit the '''Free text:''' of the page

{{{standard input|free text|rows=10}}}

{{{standard input|summary}}}

{{{standard input|minor edit}}} {{{standard input|watch}}}

{{{standard input|save}}} {{{standard input|preview}}} {{{standard input|changes}}} {{{standard input|cancel}}}
</includeonly>
PAGE3

$bot->edit({
    page    => 'Form:Car',
    summary => 'The form',
    text    => $car_form_text,
	       });





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
|Name=$fields[0]
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






