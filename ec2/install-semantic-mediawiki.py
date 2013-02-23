#!/usr/bin/env python
#License = http://en.wikipedia.org/wiki/WTFPL

import os.path
import sys
import os, errno
import random
import string
import traceback

import smwinstaller



import httplib
def getsetting(name):
    conn = httplib.HTTPConnection('169.254.169.254')
    conn.request("GET", "/latest/meta-data/%s" % name)
    #socket.error
    r1 = conn.getresponse()
    result = r1.read()
    print 'got',r1.status, r1.reason, name, result
    return result


import socket
def getpublichostname():
    if 'vagrant' not in socket.gethostname():
        try:
            return getsetting('public-hostname')
        except:
            pass

    return socket.gethostname()

def getinternalhostname():
    if 'vagrant' not in socket.gethostname():
        try:
            return getsetting('local-hostname')
        except:
            pass
    return 'localhost'

def getip():
    if 'vagrant' not in socket.gethostname():
        try:
            return getsetting('local-ipv4')
        except:
            pass
    return '127.0.0.1'


#################################################################

def init():

    global dbname
    global hostnameinternal
    global publichostname
    global hostip
    global wikiuser
    global userpassword
    global dbadminuser
    global dbadminpass
    global localsettingsfile

    global apacheconftext
    global semsettingstext
    global robotstext
    global localsettingstext
    global wikiAdminuser
    global wikiAdminpass

    global unixadminuser
    global unixuser

    global sysop
    global wikiname
    global email

    publichostname = getpublichostname()
    hostnameinternal = getinternalhostname()
    hostip = getip()

    print publichostname
    print hostnameinternal
    print hostip


    email = 'admin@example.com'
    sysop = 'Cariaso'
    wikiname = 'MySMW'

    dbname = 'my_smw'
    unixadminuser = 'ec2-user'
    unixuser = 'vagrant'


    dbadminuser = 'root'
    dbadminpass = ''


    wikiuser = 'wikiuser'
    userpassword = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))

    wikiAdminuser = 'wikiadmin'
    wikiAdminpass = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))

    localsettingsfile = '/var/www/html/LocalSettings.php'


    adict = {
        'host': hostnameinternal,
        'hostip': hostip,
        'userpassword': userpassword,
        'dbserver': hostnameinternal,
        'dbhost': hostnameinternal,
        'dbname': dbname,
        'wikiuser':wikiuser,
        'dbadminpass': dbadminpass,
        'dbadminuser': dbadminuser, 

        'wikiAdminuser': wikiAdminuser, 
        'wikiAdminpass': wikiAdminpass,
        'hostname': publichostname,
        'email':email,
        'wikiname':wikiname,
    }
    #print adict

    semsettingstext = '''
<?php

/**
 * SemanticBundle - A pre-packaged bundle of extensions meant to be used on wikis
 * based around the Semantic MediaWiki extension.
 *
 * Sample of the settings file for the Semantic Bundle
 *
 * @link https://www.mediawiki.org/wiki/Extension:Semantic_Bundle Documentation
 *
 * @file SemanticBundleSettings.php
 * @ingroup SemanticBundle
 */

if ( !defined( 'MEDIAWIKI' ) ) {
    echo "This file is not a valid entry point.";
    exit( 1 );
}

# Semantic MediaWiki basic installation.
# More info: http://semantic-mediawiki.org/wiki/Help:Installation
#include_once( "$IP/extensions/Validator/Validator.php" );
include_once( "$IP/extensions/SemanticMediaWiki/SemanticMediaWiki.php" );
#enableSemantics( parse_url( $wgServer, PHP_URL_HOST ) );

# Semantic Result Formats
# More info: http://semantic-mediawiki.org/wiki/Help:Semantic_Result_Formats#Installation
#include_once( "$IP/extensions/SemanticResultFormats/SemanticResultFormats.php" );

# Semantic Forms
# More info: https://www.mediawiki.org/wiki/Extension:Semantic_Forms
#include_once( "$IP/extensions/SemanticForms/SemanticForms.php" );

# Semantic Forms Inputs
# More info: https://www.mediawiki.org/wiki/Extension:Semantic_Forms_Inputs
#include_once( "$IP/extensions/SemanticFormsInputs/SemanticFormsInputs.php" );

# Semantic Compound Queries
# More info: https://www.mediawiki.org/wiki/Extension:Semantic_Compound_Queries
#include_once( "$IP/extensions/SemanticCompoundQueries/SemanticCompoundQueries.php" );

# Semantic Drilldown
# More info: https://www.mediawiki.org/wiki/Extension:Semantic_Drilldown#Installation
#include_once( "$IP/extensions/SemanticDrilldown/SemanticDrilldown.php" );

# Maps and Semantic Maps 
# If you're planning to use Google Maps or Yahoo! Maps, you should also set
# $egGoogleMapsKey or $egYahooMapsKey (AFTER the include_once statements).
# More info:
# http://mapping.referata.com/wiki/Maps#Installation
# http://mapping.referata.com/wiki/Semantic_Maps#Installation
#include_once( "$IP/extensions/Maps/Maps.php" );
#include_once( "$IP/extensions/SemanticMaps/SemanticMaps.php" );

# Semantic Tasks
# More info: https://www.mediawiki.org/wiki/Extension:Semantic_Tasks#Installation
#include_once( "$IP/extensions/SemanticTasks/SemanticTasks.php" );

# Semantic Internal Objects
# More info: https://www.mediawiki.org/wiki/Extension:Semantic_Internal_Objects
#include_once( "$IP/extensions/SemanticInternalObjects/SemanticInternalObjects.php" );

# Semantic Image Input
# More info: https://www.mediawiki.org/wiki/Extension:Semantic_Image_Input
#include_once( "$IP/extensions/SemanticImageInput/SemanticImageInput.php" );

# Admin Links
# More info: https://www.mediawiki.org/wiki/Extension:Admin_Links#Installation
#include_once( "$IP/extensions/AdminLinks/AdminLinks.php" );

# Approved Revs
# More info: https://www.mediawiki.org/wiki/Extension:Approved_Revs#Installation
#include_once( "$IP/extensions/ApprovedRevs/ApprovedRevs.php" );

# Arrays
# More info: https://www.mediawiki.org/wiki/Extension:Arrays#Installation
#include_once( "$IP/extensions/Arrays/Arrays.php" );

# Data Transfer
# More info: https://www.mediawiki.org/wiki/Extension:Data_Transfer#Installation
#include_once( "$IP/extensions/DataTransfer/DataTransfer.php" );

# External Data
# More info: https://www.mediawiki.org/wiki/Extension:External_Data#Installation
#include_once( "$IP/extensions/ExternalData/ExternalData.php" );

# Header Tabs
# More info: https://www.mediawiki.org/wiki/Extension:Header_Tabs#Installation
#include_once( "$IP/extensions/HeaderTabs/HeaderTabs.php" );

# Page Schemas
# More info: https://www.mediawiki.org/wiki/Extension:Page_Schemas#Installation
#require_once( "$IP/extensions/PageSchemas/PageSchemas.php" );

# Replace Text
# More info: https://www.mediawiki.org/wiki/Extension:Replace_Text#Installation
#require_once( "$IP/extensions/ReplaceText/ReplaceText.php" );

# Widgets
# Also need to do some permission setup: http://www.mediawiki.org/wiki/Extension:Widgets#Folder_permissions
# More info: https://www.mediawiki.org/wiki/Extension:Widgets#Installation
#require_once( "$IP/extensions/Widgets/Widgets.php" );
#$wgGroupPermissions['sysop']['editwidgets'] = true;
'''

    apacheconftext = ''




    robotstext = '''
# robots are awesome
'''

    localsettingstext = """<?php

# Further documentation for configuration settings may be found at:
# http://www.mediawiki.org/wiki/Manual:Configuration_settings


# Protect against web entry
if ( !defined( 'MEDIAWIKI' ) ) {
        exit;
}

$wgSitename         = "%(wikiname)s";

## The URL base path to the directory containing the wiki;
## defaults for all runtime URL paths are based off of this.
## For more information on customizing the URLs please see:
## http://www.mediawiki.org/wiki/Manual:Short_URL
$wgScriptPath       = "";
$wgScriptExtension  = ".php";






## The protocol and server name to use in fully-qualified URLs
$wgServer           = "http://%(hostname)s";

## The relative URL path to the skins directory
$wgStylePath        = "$wgScriptPath/skins";

## The relative URL path to the logo.  Make sure you change this from the default,
## or else you'll overwrite your logo when you upgrade!
$wgLogo             = "$wgStylePath/common/images/wiki.png";

## UPO means: this is also a user preference option

$wgEnableEmail      = true;
$wgEnableUserEmail  = true; # UPO


$wgEnotifUserTalk = true; # UPO
$wgEnotifWatchlist = true; # UPO
$wgEmailAuthentication = true;


$wgEmergencyContact = "%(email)s";
$wgPasswordSender   = "%(email)s";


# If PHP's memory limit is very low, some operations may fail.
ini_set( 'memory_limit', '200M' );




## Database settings

$wgDBadminuser      = '%(wikiAdminuser)s';
$wgDBadminpassword  = '%(wikiAdminpass)s';

$wgDBtype           = "mysql";
$wgDBserver         = "%(dbserver)s";
$wgDBname           = "%(dbname)s";
$wgDBuser           = "%(wikiuser)s";
$wgDBpassword       = "%(userpassword)s";

# MySQL specific settings
$wgDBprefix         = "";


# MySQL table options to use during installation or update
#$wgDBTableOptions   = "ENGINE=InnoDB, DEFAULT CHARSET=binary";
$wgDBTableOptions   = "ENGINE=InnoDB, DEFAULT CHARSET=utf8";

# Experimental charset support for MySQL 4.1/5.0.
$wgDBmysql5 = true;

## Shared memory settings
$wgMainCacheType = CACHE_NONE;
$wgMemCachedServers = array();


## To enable image uploads, make sure the 'images' directory
## is writable, then set this to true:
$wgEnableUploads       = true;
$wgUseImageMagick = true;
$wgImageMagickConvertCommand = "/usr/bin/convert";

## If you use ImageMagick (or any other shell command) on a
## Linux server, this will need to be set to the name of an
## available UTF-8 locale
$wgShellLocale = "en_US.utf8";

## If you have the appropriate support software installed
## you can enable inline LaTeX equations:
$wgUseTeX           = false;

## Set $wgCacheDirectory to a writable directory on the web server
## to make your wiki go slightly faster. The directory should not
## be publically accessible from the web.
#$wgCacheDirectory = "$IP/cache";

$wgLocalInterwiki   = strtolower( $wgSitename );

$wgLanguageCode = "en";

$wgSecretKey = "3567eydrtg6ydhg4ysehtysehdrfuy434352912982189734sehxrctfu5dtrjytfy5dutuy";

## Default skin: you can change the default skin. Use the internal symbolic
## names, ie 'vector', 'monobook':
$wgDefaultSkin = 'vector';



## For attaching licensing metadata to pages, and displaying an
## appropriate copyright notice / icon. GNU Free Documentation
## License and Creative Commons licenses are supported so far.
# $wgEnableCreativeCommonsRdf = true;
$wgRightsPage = ""; # Set to the title of a wiki page that describes your license/copyright
$wgRightsUrl = "";
$wgRightsText = "";
$wgRightsIcon = "";
# $wgRightsCode = ""; # Not yet used

$wgDiff3 = "/usr/bin/diff3";

# When you make changes to this configuration file, this will make
# sure that cached pages are cleared.
$wgCacheEpoch = max( $wgCacheEpoch, gmdate( 'YmdHis', @filemtime( __FILE__ ) ) );


$wgShowExceptionDetails = true;


require_once( "$IP/extensions/ParserFunctions/ParserFunctions.php" );

require_once( "$IP/extensions/ConfirmEdit/ConfirmEdit.php" );
require_once( "$IP/extensions/ConfirmEdit/QuestyCaptcha.php" );
$wgCaptchaClass = 'QuestyCaptcha';
$wgCaptchaQuestions[] = array( 'question' => "captcha question not yet set. I'm thinking of a number. ", 'answer' => "58398348734" );
$wgCaptchaQuestions[] = array( 'question' => "how many editors does it take to screw in a lightbulb", 'answer' => "3341" );

//These were no longer effective against spammers
//require_once( "$IP/extensions/recaptcha/ReCaptcha.php" );
//// Sign up for these at http://recaptcha.net/api/getkey
//// amazonaws.com keys
//$recaptcha_public_key = '634567898765445678987654345678765';
//$recaptcha_private_key = '6456787654345678765434567654345Mp';



// Fix the default captcha behaviour
$wgGroupPermissions['*'            ]['skipcaptcha'] = false;
$wgGroupPermissions['user'         ]['skipcaptcha'] = true;
$wgGroupPermissions['autoconfirmed']['skipcaptcha'] = true;
$wgGroupPermissions['bot'          ]['skipcaptcha'] = true; // registered bots
$wgGroupPermissions['sysop'        ]['skipcaptcha'] = true;


$wgCaptchaTriggers['edit']          = true;
$wgCaptchaTriggers['create']        = true;
$wgCaptchaTriggers['addurl']        = true;  // Check on edits that add URLs
$wgCaptchaTriggers['createaccount'] = true;



$wgUseAjax = true;


#require_once( "$IP/extensions/Validator/Validator.php" );
require_once( "$IP/extensions/SemanticBundle/SemanticBundleSettings.php" );
require_once( "$IP/extensions/SemanticBundle/SemanticBundle.php" );
#include_once("$IP/extensions/SemanticMediaWiki/SemanticMediaWiki.php");
#enableSemantics('mysite.com');


$smwgAdminRefreshStore = true;

$smwgEnableTemplateSupport = true;



#include_once("$IP/extensions/SemanticForms/SemanticForms.php");

#$wgJobRunRate = 0.01;

$wgFileExtensions = array( 'png', 'jpg', 'jpeg', 'ppt','ogg','pdf');

$wgNamespacesWithSubpages[NS_MAIN] = true;



#include_once("$IP/extensions/SemanticInternalObjects/SemanticInternalObjects.php");
#include_once("$IP/extensions/SemanticResultFormats/SemanticResultFormats.php");



require_once( "$IP/extensions/ReplaceText/ReplaceText.php" );

$wgGroupPermissions['sysop']['replacetext'] = true;



$wgDisableCounters = true;

#$wgShowExceptionDetails = true;

$wgShowIPinHeader = false;

require_once( "$IP/extensions/TitleBlacklist/TitleBlacklist.php" );

$wgSpamRegex = "/worldselectshop|ameritrust|truthaboutabsreviewscam|findthisall.com|YesMyBride|vistastemcell/";

require_once("$IP/extensions/Survey/Survey.php" );
require_once("$IP/extensions/Nuke/Nuke.php");





#require_once( "$IP/extensions/googleAnalytics/googleAnalytics.php" );
#$wgGoogleAnalyticsAccount = "UA-123456-7";
#$wgGoogleAnalyticsIgnoreBots = false;
#$wgGoogleAnalyticsAddASAC = true;




#$wgDebugLogFile = '/tmp/mwlog.txt';
#$wgShowExceptionDetails = true;

#include_once("$IP/extensions/SemanticDrilldown/SemanticDrilldown.php");
$sdgHideCategoriesByDefault = true;
$sdgFiltersSmallestFontSize=9;
$sdgFiltersLargestFontSize=25;

# necessary for bot semanticforms writes
#$wgParserConf['preprocessorClass'] = 'Preprocessor_Hash';


""" % adict

                                                                                                                        

try:
    from fabric.api import run, put, cd, lcd, env, get, sudo, settings
    from fabric.contrib.files import exists, append, contains
    from fabric.decorators import hosts, task
    from fabric.operations import local
    import fabric
except ImportError:
    print 'without fabric this program is a bit limited. try "pip install fabric"'


def put_text_to_file(text, filename):

    atmpfn = 'a_tmp_file'
    f = file(atmpfn, 'w')
    f.write(text)
    f.close()
    try:
        put(atmpfn, filename)
    except:
        remotefn = 'a_tmp2_file'
        sudo('chown %s:%s %s' % (unixuser, unixuser, filename), pty=True)
        sudo('chmod g+w %s' % filename, pty=True)
        put(atmpfn, remotefn)
        run('mv %s %s' % (remotefn, filename))

    os.unlink(atmpfn)


def put_text_to_local_file(text, filename):
    f = file(filename, 'w')
    f.write(text)
    f.close()


def localize():
    global sudo
    global run
    global exists
    global put_text_to_file
    global cd

    #orig_run = run


    orig_sudo = sudo
    def sudo(cmd, pty=None, user=None):
        return local(cmd)

    orig_exists = exists
    def exists(path):
        return os.path.exists(os.path.join(env.lcwd,path))

    run = local
    #sudo = local_sudo
    #exists = local_exists
    put_text_to_file = put_text_to_local_file
    cd = lcd


def setup_wiki():

    

    if not exists('/var/www'):
        sudo('mkdir -p /var/www')
    sudo('chown %s:%s /var/www' % (unixuser, unixuser), pty=True)

    if not exists('/var/www/html'):
        sudo('mkdir -p /var/www/html')
        sudo('chown %s:%s /var/www/html'  % (unixuser, unixuser), pty=True)

    if exists('/var/lib/php/session'):
        sudo('chmod a+rwx /var/lib/php/session')

    sudo('yum -y install subversion git')


    with cd('/var/www'):
        sudo('chown %s:%s html'  % (unixuser, unixuser), pty=True)

        tgzver = 'mediawiki-1.20.2.tar.gz'
        tgzurl = 'http://download.wikimedia.org/mediawiki/1.20/%s' % tgzver

        if not exists(tgzver):
            #just run was good enough
            sudo('wget %s' % tgzurl, user=unixuser)
        else:
            pass


        if not exists('html/maintenance'):
            with settings(warn_only=True):

                run('pwd')
                run('ls -tral')
                sudo('tar -zxv -C html --strip-components 1 -f %s' % tgzver, user=unixuser)
        
        #if not exists('html/.git'):
        #    run('git clone https://gerrit.wikimedia.org/r/p/mediawiki/core.git html')

        with cd('html'):

            if exists('.git'):
                run('git checkout origin/REL1_20')

            with settings(
                user=unixuser,
                ):

                
                put_text_to_file(robotstext, '/var/www/html/robots.txt')
                if not exists('extensions'):
                    run('mkdir -p extensions')

                with cd('extensions'):

                    if not exists('googleAnalytics'):
                        run('svn co http://svn.wikimedia.org/svnroot/mediawiki/trunk/extensions/googleAnalytics')
                    else:
                        with cd('googleAnalytics'):
                            run('svn update')

                    for extension in [
                        'SemanticMediaWiki',

                        #'SemanticDrilldown',
                        #'SemanticForms',
                        'ConfirmEdit',
                        'ParserFunctions',
                        #'SemanticInternalObjects',
                        'Validator',
                        'DataValues',
                        'SemanticBundle',
                        #'SemanticResultFormats',
                        'ReplaceText',
                        'TitleBlacklist',
                        'Survey',
                        'Nuke',
                        'GoogleAdSense',
                        ]:

                        if not exists(extension):
                            run('git clone https://gerrit.wikimedia.org/r/p/mediawiki/extensions/%s.git' % extension)
                        else:
                            with cd(extension):
                                if exists('.git'):
                                    with settings(warn_only=True):
                                        run('git pull')
                                else:
                                    print "can't update %s" % extension



                    semsettingsname = '/var/www/html/extensions/SemanticBundle/SemanticBundleSettings.php'
                    put_text_to_local_file(semsettingstext, semsettingsname)


        with cd('html/maintenance'):

            with settings(
                user=unixuser,
                ):

                run('rm -f SMW_setup.php')
                run('rm -f SMW_refreshData.php')
                sudo('ln -s ../extensions/SemanticMediaWiki/maintenance/SMW_setup.php', user=unixadminuser)
                sudo('ln -s ../extensions/SemanticMediaWiki/maintenance/SMW_refreshData.php', user=unixadminuser)


def setup_webserver_step2(ALLOW_DESTROY=False):

    adict = {
        'installdbuser':dbadminuser,
        'installdbpass':dbadminpass,

        'sysop':sysop,
        'wikiname':wikiname,
        'userpass':userpassword,

        'dbname':dbname,
        'dbuser':wikiuser,
        'dbserver':hostnameinternal,
        'wikiAdminuser': wikiAdminuser, 
        'wikiAdminpass': wikiAdminpass,
        }




    with settings(user=unixadminuser):
        with cd('/var/www/html/maintenance'):
            if ALLOW_DESTROY:
                sudo('echo "drop database %(dbname)s" | mysql -u %(installdbuser)s' % adict)
                run('rm -f %s' % localsettingsfile)
            else:
                print "I'm not allowed to overwrite your database or LocalSettings.pgp. try with --destroy"

            if not exists(localsettingsfile):
                run('php /var/www/html/maintenance/install.php --installdbuser %(wikiAdminuser)s --installdbpass "%(wikiAdminpass)s" --scriptpath / --dbuser %(dbuser)s --pass "%(userpass)s" --dbtype mysql --dbserver %(dbserver)s --dbname %(dbname)s  %(wikiname)s %(sysop)s' % adict)

        print "updating %s" % localsettingsfile
        put_text_to_file(localsettingstext, localsettingsfile)




    with cd('/var/www/html/maintenance'):
        if exists(localsettingsfile):
            run('php update.php --quick')

    run('apachectl restart')






def setup_mysql():

    sudo('yum -y install mysql mysql-server', pty=True)
    sudo('service mysqld restart', pty=True)


    adict = {

        'toadminuser': dbadminuser,
        'toadminpass': dbadminpass,
        'todb':dbname,
        'tohost':hostnameinternal,

        'wikiusername': wikiuser,
        'wikiuserpass': userpassword,
        'hostinternal': hostnameinternal,



        }

    #mysqlcmd = 'echo mysql -u %(toadminuser)s --password=\'%(toadminpass)s\' -h %(todb)s.%(tohost)s ''' % adict
    mysqlcmd = 'mysql -u %(toadminuser)s --password=\'%(toadminpass)s\' ''' % adict
    adict['mysqlcmd'] = mysqlcmd

    try:
        run('echo "create database %(todb)s;" | %(mysqlcmd)s' % adict)                                                                                                                       
    except:
        print "unable to create the db"


    run('''echo "grant index, create, select, insert, update, delete, alter, lock tables on %(todb)s.* to '%(wikiusername)s'@'%(hostinternal)s' identified by '%(wikiuserpass)s';" | %(mysqlcmd)s''' % adict)                                                                                                                                                                     


    adict['toadminuser'] = wikiAdminuser
    adict['toadminpass'] = wikiAdminpass

    run('echo "GRANT ALL PRIVILEGES ON %(todb)s.* TO \'%(toadminuser)s\'@\'%(hostinternal)s\' IDENTIFIED BY \'%(toadminpass)s\' with GRANT OPTION;"  | %(mysqlcmd)s' % adict)



def setup_httpd():

    sudo('yum -y install httpd httpd-devel', pty=True)

    sudo("perl -p -i.bak -e 's!AddType\s+application/x-httpd-php\s+.php!!' /etc/httpd/conf/httpd.conf", pty=True)
    sudo("perl -p -i.bak -e 's!(AddType\s+application/x-tar\s+\.tgz)!$1\\nAddType application/x-httpd-php .php!' /etc/httpd/conf/httpd.conf", pty=True)

    sudo("perl -p -i.bak -e 's!^DirectoryIndex.*!DirectoryIndex index.html index.php!' /etc/httpd/conf/httpd.conf", pty=True)


    if apacheconftext:
        if not exists('/etc/httpd/conf.d'):
            sudo('mkdir -p /etc/httpd/conf.d', pty=True)

        localname = '/tmp/httpd-conf-semanticmediawiki.conf'
        put_text_to_local_file(apacheconftext, localname)

        try:
            sudo('mv %s /etc/httpd/conf.d/semanticmediawiki.conf' % localname, pty=True)
                 
        except:
            pass



def setup_php():
    sudo('yum -y install php-devel php-pear php-pecl-apc php php-mysql php-xml', pty=True)


def main(argv=[]):
    init()
    parameters = smwinstaller.loadParameters(argv)
    if parameters.debug:
        print parameters
        try:
            localize()
            setup_mysql()
            setup_php()
            setup_httpd()
            setup_wiki()
            setup_webserver_step2(ALLOW_DESTROY=parameters.destroy)
        except Exception, e:
            traceback.print_exc()                                                                                                                                                            
            print "crap %s" % e
            traceback.print_stack()


    print '%s : %s' % (sysop, userpassword)
    print '%s : %s' % (wikiAdminuser, wikiAdminpass)



if __name__ == '__main__':

    main(sys.argv)
