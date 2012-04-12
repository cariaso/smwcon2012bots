Most pywikipediabots have a user-config.py and a
families/{familyname}_family.py file, which lives external to any bot,
and must be setup in advance. This directory is an example of that. It
is still uncommon to modify sys.path and import from a non-installed
directory, but I don't want to permanently alter anything on your
system during this talk.