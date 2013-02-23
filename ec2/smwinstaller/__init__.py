#!/usr/bin/env python
#License = http://en.wikipedia.org/wiki/WTFPL

import os.path
import sys
import os, errno
import random
import string

def parseYamlConfig(parameters):
    try:
        import yaml
    except ImportError, e:
        print "unable to import yaml"
        return parameters

    f = open(parameters.yamlconfig)
    dataMap = yaml.load(f)
    f.close()
    for k in dataMap:
        if not hasattr(parameters, k):
            setattr(parameters, k, dataMap[k])
    return parameters

def simpleArgParser(argv):
    print 'without argparse this program is a bit limited on command line options. try "pip install argparse"'
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-n', '--new', help='creates a new object')
    parser.add_option('-d', '--debug', help='debug mode')
    parser.add_option('-d', '--destroy', help='allowed to overwrite the database and the LocalSettings.php file')
    (opts, args) = parser.parse_args()
    return opts

def loadParameters(argv):
    '''
    Load from command line switches or a YAML file, return a single dictionary
    '''

    try:
        import argparse
    except ImportError:
        return simpleArgParser(argv)




    parser = argparse.ArgumentParser(
        description="install semantic-mediawiki",
        epilog="Michael Cariaso "
        "cariaso@gmail.com "
        "License = http://en.wikipedia.org/wiki/WTFPL"
        )
    
    group_std1 = parser.add_argument_group(title="Main",
                                           description="Primary Options"
                                           )
    

    group_mysql1 = parser.add_argument_group(title="MySQL",
                                           description="usernames password hosts"
                                           )
    group_unix1 = parser.add_argument_group(title="Unix",
                                           description="usernames paths"
                                           )
    
    group_std1.add_argument("--destroy",
                            help="blow away the database and the LocalSettings.php file",
                            action="store_true",
                            default=False,
                            )


    group_std1.add_argument("--wikiname",
                            help="shortname for your wiki",
                            type=str,
                            default='MySMW',
                            )
    group_std1.add_argument("--email",
                            help="contact email address",
                            type=str,
                            default='admin@example.com',
                            )

    group_std1.add_argument("--sysop",
                            help="first admin user wiki username",
                            type=str,
                            default='WikiAdmin',
                            )



    group_unix1.add_argument("--unixadminuser",
                            help='user who can sudo',
                            type=str,
                            default='ec2-user')
    group_unix1.add_argument("--unixuser",
                            help='user who will own the unix installation',
                            type=str,
                            default='vagrant')


    group_mysql1.add_argument("--dbname",
                            help='mysql database name',
                            type=str,
                            default='my_smw',
                            )

    group_mysql1.add_argument("--dbadminuser",
                            help='mysql username allowed to create other users',
                            type=str,
                            default='root')
    group_mysql1.add_argument("--dbadminpass",
                            help='password for dbadminuser',
                            type=str,
                            default='')


    group_mysql1.add_argument("--wikiAdminuser",
                            help='this mysql account will be created and given the ability to create tables',
                            type=str,
                            default='wikiadmin')
    group_mysql1.add_argument("--wikiAdminpass",
                            help='you can override the randomly chosen one',
                            type=str,
                            default=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                            )

    group_mysql1.add_argument("--wikiuser",
                            help='this mysql is used by the wiki to read and write to the database',
                            type=str,
                            default='wikiuser')
    group_mysql1.add_argument("--userpassword",
                            help='you can override the randomly chosen ones',
                            type=str,
                            default=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                           )



    group_std1.add_argument("--localsettingsfile",
                            help='',
                            type=str,
                            default='/var/www/html/LocalSettings.php')

    group_std1.add_argument("--yamlconfig",
                            help="this config file can replace all of the other command line settings",
                            type=str,
                            )








    group_exper1 = parser.add_argument_group(title="Experimental",
                                           description="Experimental Options"
                                           )
    
    group_exper1.add_argument("--debug",
                            help="debug mode, helpful for developers",
                            action="store_true",
                            default=False,
                            )



    parameters, unknown = parser.parse_known_args(argv)
    parameters.unknown = unknown

    if parameters.yamlconfig:
        print "got yaml file"
        parameters = parseYamlConfig(parameters)

    return parameters

def test(argv=[]):

    parameters = loadParameters(argv)
    if parameters.debug:
        print parameters


if __name__ == '__main__':
    test(sys.argv)
