#!/usr/bin/env python
#License = http://en.wikipedia.org/wiki/WTFPL

import os.path
import sys
import os, errno

import smwinstaller



def main(argv=[]):

    parameters = smwinstaller.loadParameters(argv)
    if parameters.debug:
        print parameters

        setup_wiki()
        setup_webserver_step2()


#################################################################



snpediadbmachine = 'localhost'
snpediadbhost = ''
userpassword = ''
snpediadbname = ''
wikiadminpassword = ''
hostinternal = ''
hostip = ''
wikiadminuser = ''


apacheconftext = '''

'''

robotstext = '''
# robots are awesome
'''

localsettingstext = """<?php

# Further documentation for configuration settings may be found at:
# http://www.mediawiki.org/wiki/Manual:Configuration_settings

# If you customize your file layout, set $IP to the directory that contains
# the other MediaWiki files. It will be used as a base to locate files.
if( defined( 'MW_INSTALL_PATH' ) ) {
        $IP = MW_INSTALL_PATH;
} else {
        $IP = dirname( __FILE__ );
}

$path = array( $IP, "$IP/includes", "$IP/languages", "/usr/share/php" );
set_include_path( implode( PATH_SEPARATOR, $path ) . PATH_SEPARATOR . get_include_path() );

require_once( "$IP/includes/DefaultSettings.php" );

# If PHP's memory limit is very low, some operations may fail.
ini_set( 'memory_limit', '200M' );

if ( $wgCommandLineMode ) {
        if ( isset( $_SERVER ) && array_key_exists( 'REQUEST_METHOD', $_SERVER ) ) {
                die( "This script must be run from the command line\n" );
        }
}
## Uncomment this to disable output compression
# $wgDisableOutputCompression = true;

$wgSitename         = "MySMW";

## The URL base path to the directory containing the wiki;
## defaults for all runtime URL paths are based off of this.
## For more information on customizing the URLs please see:
## http://www.mediawiki.org/wiki/Manual:Short_URL
$wgScriptPath       = "";
$wgScriptExtension  = ".php";

## The relative URL path to the skins directory
$wgStylePath        = "$wgScriptPath/skins";


## The relative URL path to the logo.  Make sure you change this from the default,
## or else you'll overwrite your logo when you upgrade!
$wgLogo             = "$wgStylePath/common/images/wiki.png";

## UPO means: this is also a user preference option

$wgEnableEmail      = true;
$wgEnableUserEmail  = true; # UPO

$wgEmergencyContact = "info@example.com";
$wgPasswordSender = "info@example.com";

$wgEnotifUserTalk = true; # UPO
$wgEnotifWatchlist = true; # UPO
$wgEmailAuthentication = true;

## Database settings

$wgDBadminuser      = '%(wikiadminuser)s';
$wgDBadminpassword  = '%(wikiadminpassword)s';

$wgDBtype           = "mysql";
$wgDBserver         = "%(dbhost)s";
$wgDBname           = "%(dbname)s";
$wgDBuser           = "wikiuser";
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


require_once( "$IP/extensions/Validator/Validator.php" );
include_once("$IP/extensions/SemanticMediaWiki/SemanticMediaWiki.php");
enableSemantics('mysite.com');


# enable http://www.snpedia.com/index.php/Special:SMWAdmin?action=refreshstore
$smwgAdminRefreshStore = true;

$smwgEnableTemplateSupport = true;



include_once("$IP/extensions/SemanticForms/SemanticForms.php");

#$wgJobRunRate = 0.01;

$wgFileExtensions = array( 'png', 'jpg', 'jpeg', 'ppt','ogg','pdf');

$wgNamespacesWithSubpages[NS_MAIN] = true;



include_once("$IP/extensions/SemanticInternalObjects/SemanticInternalObjects.php");
include_once("$IP/extensions/SemanticResultFormats/SemanticResultFormats.php");



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
$wgParserConf['preprocessorClass'] = 'Preprocessor_Hash';


""" % {
        'dbmachine': snpediadbmachine,
        'dbhost': snpediadbhost,
        'userpassword': userpassword,
        'dbname': snpediadbname,
        'wikiadminpassword': wikiadminpassword,
        'host': hostinternal,
        'hostip': hostip,
        'wikiadminuser': wikiadminuser,
    }

                                                                                                                        

from fabric.api import run, put, cd, lcd, env, get, sudo, settings
from fabric.contrib.files import exists, append, contains
from fabric.decorators import hosts, task
from fabric.operations import local
import fabric


def put_text_to_file(text, filename):

    atmpfn = 'a_tmp_file'
    f = file(atmpfn, 'w')
    f.write(text)
    f.close()
    try:
        put(atmpfn, filename)
    except:
        remotefn = 'a_tmp2_file'
        sudo('chown ec2-user:ec2-user %s' % filename, pty=True)
        sudo('chmod g+w %s' % filename, pty=True)
        put(atmpfn, remotefn)
        run('mv %s %s' % (remotefn, filename))

    os.unlink(atmpfn)


def put_text_to_local_file(text, filename):
    f = file(filename, 'w')
    f.write(text)
    f.close()


def setup_wiki():

    global sudo
    global run
    global exists
    orig_sudo = sudo
    orig_run = run
    orig_exists = exists


    def local_sudo(cmd, pty=None, user=None):
        return local(cmd)

    def local_exists(path):
        return os.path.exists(os.path.join(env.lcwd,path))

    run = local
    sudo = local_sudo
    exists = local_exists
    put_text_to_file = put_text_to_local_file
    cd = lcd




    setup_httpd()
    setup_php()
    # but https://forums.aws.amazon.com/thread.jspa?threadID=99754
    #if not exists('/usr/lib64/php/modules/apc.so'):
    #    sudo('yum -y remove *php*', pty=True)
    #    sudo('yum -y install php php-devel php-pear php-pecl-apc php-mysql php-pdo php-gd php-cli php-common', pty=True)






    if not exists('/var/www'):
        sudo('mkdir -p /var/www')
    sudo('chown ec2-user:ec2-user /var/www', pty=True)

    if not exists('/var/www/html'):
        sudo('mkdir -p /var/www/html')
        #sudo('chown ec2-user:ec2-user /var/www/html', pty=True)

    if exists('/var/lib/php/session'):
        sudo('chmod a+rwx /var/lib/php/session')

    sudo('yum -y install subversion git')

    with cd('/var/www'):
        #sudo('chown ec2-user:ec2-user html', pty=True)

        tgzver = 'mediawiki-1.20.2.tar.gz'
        tgzurl = 'http://download.wikimedia.org/mediawiki/1.20/%s' % tgzver
        import pdb
        pdb.set_trace()

        if not exists(tgzver):
            #just run was good enough
            sudo('wget %s' % tgzurl, user='ec2-user')
        else:
            pass


        if not exists('html/maintenance'):
            #run('mkdir -p libs')
            with settings(warn_only=True):

                run('pwd')
                run('ls -tral')
                sudo('tar -zxv -C html --strip-components 1 -f %s' % tgzver, user='ec2-user')
        
        #if not exists('html/.git'):
        #    run('git clone https://gerrit.wikimedia.org/r/p/mediawiki/core.git html')

        with cd('html'):

            if exists('.git'):
                #run('git checkout origin/REL1_19')
                run('git checkout origin/REL1_20')
            #google_patch_mediawiki()

            with settings(
                user='ec2-user',
                ):

                
                put_text_to_file(robotstext, '/var/www/html/robots.txt')
                put_text_to_file(
                    localsettingstext, '/var/www/html/LocalSettings.php')


                if not exists('extensions'):
                    run('mkdir -p extensions')

                with cd('extensions'):

                    if not exists('googleAnalytics'):
                        run('svn co http://svn.wikimedia.org/svnroot/mediawiki/trunk/extensions/googleAnalytics')
                    else:
                        with cd('googleAnalytics'):
                            run('svn update')

                    for extension in ['SemanticDrilldown',
                                      'SemanticForms',
                                      'ConfirmEdit',
                                      'ParserFunctions',
                                      'SemanticInternalObjects',
                                      'Validator',
                                      'DataValues',
                                      'SemanticMediaWiki',
                                      'SemanticResultFormats',
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





        with cd('html'):

            with settings(
                user='ec2-user',
                ):

                with cd('extensions'):

                    for extension, fetchname, gitversion in [
                        ('SemanticMediaWiki', '1.8.x:1.8.x', '7317d89'), #'414f1d4' fails
                        ('SemanticForms', None, '7317d89'), #


                        ]:

                        with settings(warn_only=True):
                            with cd(extension):
                                if fetchname:
                                    run('git fetch origin %s' % fetchname)
                                run('git checkout %s' % gitversion)











                with cd('maintenance'):
                    run('rm -f SMW_setup.php')
                    run('rm -f SMW_refreshData.php')
                    sudo('ln -s ../extensions/SemanticMediaWiki/maintenance/SMW_setup.php', user='ec2-user')
                    sudo('ln -s ../extensions/SemanticMediaWiki/maintenance/SMW_refreshData.php', user='ec2-user')

def setup_webserver_step2():

    with cd('/var/www/html/maintenance'):
        run('php update.php --quick')

    with cd('/var/www/html/maintenance'):
        try:
            run('php SMW_setup.php')
        except:
            print "php SMW_setup.php crapped out"

    print "restart_webserver()"



def setup_httpd():
    sudo('yum -y install httpd httpd-devel', pty=True)

    sudo("perl -p -i.bak -e 's!AddType\s+application/x-httpd-php\s+.php!!' /etc/httpd/conf/httpd.conf", pty=True)
    sudo("perl -p -i.bak -e 's!(AddType\s+application/x-tar\s+\.tgz)!$1\\nAddType application/x-httpd-php .php!' /etc/httpd/conf/httpd.conf", pty=True)

    sudo("perl -p -i.bak -e 's!^DirectoryIndex.*!DirectoryIndex index.html index.php!' /etc/httpd/conf/httpd.conf", pty=True)

    if not exists('/etc/httpd/conf.d'):
        sudo('mkdir -p /etc/httpd/conf.d', pty=True)

    localname = '/tmp/httpd-conf-semanticmediawiki.conf'
    put_text_to_local_file(apacheconftext, localname)

    try:
        sudo('mv %s /etc/httpd/conf.d/semanticmediawiki.conf' % localname,
             pty=True)
    except:
        pass



def setup_php():
    sudo('yum -y install php-devel php-pear php-pecl-apc', pty=True)








if __name__ == '__main__':
    main(sys.argv)
