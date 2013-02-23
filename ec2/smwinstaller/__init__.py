#!/usr/bin/env python
#License = http://en.wikipedia.org/wiki/WTFPL

import os.path
import sys
import os, errno


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
    
    group_std1.add_argument("--yamlconfig",
                            help="config file",
                            type=str,
                            )

    group_std1.add_argument("--destroy",
                            help="allowed to blow away the database and the LocalSettings.php file",
                            action="store_true",
                            default=False,
                            )


    group_std1.add_argument("--sysop",
                            help="first admin user wiki username",
                            type=str,
                            default='WikiAdmin',
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
    group_std1.add_argument("--dbname",
                            help='',
                            type=str,
                            default='my_smw',
                            )
    group_std1.add_argument("--unixadminuser",
                            help='',
                            type=str,
                            default='ec2-user')
    group_std1.add_argument("--unixuser",
                            help='',
                            type=str,
                            default='vagrant')
    group_std1.add_argument("--dbadminuser",
                            help='',
                            type=str,
                            default='root')
    group_std1.add_argument("--dbadminpass",
                            help='',
                            type=str,
                            default='')
    group_std1.add_argument("--wikiuser",
                            help='',
                            type=str,
                            default='wikiuser')





    group_exper1 = parser.add_argument_group(title="Experimental",
                                           description="Experimental Options"
                                           )
    
    group_exper1.add_argument("--debug",
                            help="debug mode, helpful for developers",
                            action="store_true",
                            default=False,
                            )
    group_std1.add_argument("--wikiAdminuser",
                            help='',
                            type=str,
                            default='wikiadmin')
    group_std1.add_argument("--localsettingsfile",
                            help='',
                            type=str,
                            default='/var/www/html/LocalSettings.php')



    group_std1.add_argument("--wikiAdminpass",
                            help='',
                            type=str,
                            default=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                            )
    group_std1.add_argument("--userpassword",
                            help='',
                            type=str,
                            default=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
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
