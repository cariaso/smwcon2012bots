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
    #print 'got',r1.status, r1.reason, name, result
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

def loadtemplate(templatefn):
    afile = file(templatefn,'r')
    text = afile.read()
    afile.close()
    return text


def init(parameters):

    global hostnameinternal
    global publichostname
    global hostip

    global apacheconftext
    global semsettingstext
    global robotstext
    global localsettingstext

    publichostname = getpublichostname()
    hostnameinternal = getinternalhostname()
    hostip = getip()

    print publichostname
    print hostnameinternal
    print hostip

    adict = {
        'host': hostnameinternal,
        'hostip': hostip,
        'userpassword': parameters.userpassword,
        'dbserver': hostnameinternal,
        'dbhost': hostnameinternal,
        'dbname': parameters.dbname,
        'wikiuser':parameters.wikiuser,
        'dbadminpass': parameters.dbadminpass,
        'dbadminuser': parameters.dbadminuser, 

        'wikiAdminuser': parameters.wikiAdminuser, 
        'wikiAdminpass': parameters.wikiAdminpass,
        'hostname': publichostname,
        'email':parameters.email,
        'wikiname':parameters.wikiname,
    }
    #print adict

    templatedir = 'templates'
    semsettingstemplatefn = os.path.join(templatedir, 'semanticsettings.template')
    semsettingstext = loadtemplate(semsettingstemplatefn) % adict
    localsettingstext = loadtemplate(os.path.join(templatedir, 'localsettings.template')) % adict
    robotstext = loadtemplate(os.path.join(templatedir, 'robots.template')) % adict

    apacheconftext = ''


                                                                                                                        

try:
    from fabric.api import run, put, cd, lcd, env, get, sudo, settings
    from fabric.contrib.files import exists, append, contains
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
        sudo('chown %s:%s %s' % (parameters.unixuser, parameters.unixuser, filename), pty=True)
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


def setup_mysql(parameters=None):
    if parameters is None:
        parameters={}

    sudo('yum -y install mysql mysql-server', pty=True)
    sudo('service mysqld restart', pty=True)


    adict = {

        'toadminuser': parameters.dbadminuser,
        'toadminpass': parameters.dbadminpass,
        'todb':parameters.dbname,
        'tohost':hostnameinternal,

        'wikiusername': parameters.wikiuser,
        'wikiuserpass': parameters.userpassword,
        'hostinternal': hostnameinternal,



        }

    #mysqlcmd = 'echo mysql -u %(toadminuser)s --password=\'%(toadminpass)s\' -h %(todb)s.%(tohost)s ''' % adict
    mysqlcmd = 'mysql -u %(toadminuser)s --password=\'%(toadminpass)s\'' % adict
    adict['mysqlcmd'] = mysqlcmd

    try:
        run('echo "create database %(todb)s;" | %(mysqlcmd)s' % adict)                                                                                                                       
    except:
        print "unable to create the db"


    run('''echo "grant index, create, select, insert, update, delete, alter, lock tables on %(todb)s.* to '%(wikiusername)s'@'%(hostinternal)s' identified by '%(wikiuserpass)s';" | %(mysqlcmd)s''' % adict)                                                                                                                                                                     


    adict['toadminuser'] = parameters.wikiAdminuser
    adict['toadminpass'] = parameters.wikiAdminpass

    run('echo "GRANT ALL PRIVILEGES ON %(todb)s.* TO \'%(toadminuser)s\'@\'%(hostinternal)s\' IDENTIFIED BY \'%(toadminpass)s\' with GRANT OPTION;"  | %(mysqlcmd)s' % adict)


def setup_php():
    sudo('yum -y install php-devel php-pear php-pecl-apc php php-mysql php-xml', pty=True)

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







def setup_wiki(parameters=None):
    if parameters is None:
        parameters={}

    

    if not exists('/var/www'):
        sudo('mkdir -p /var/www')
    sudo('chown %s:%s /var/www' % (parameters.unixuser, parameters.unixuser), pty=True)

    if not exists('/var/www/html'):
        sudo('mkdir -p /var/www/html')
        sudo('chown %s:%s /var/www/html'  % (parameters.unixuser, parameters.unixuser), pty=True)

    if exists('/var/lib/php/session'):
        sudo('chmod a+rwx /var/lib/php/session')

    sudo('yum -y install subversion git')


    with cd('/var/www'):
        sudo('chown %s:%s html'  % (parameters.unixuser, parameters.unixuser), pty=True)

        tgzver = 'mediawiki-1.20.2.tar.gz'
        tgzurl = 'http://download.wikimedia.org/mediawiki/1.20/%s' % tgzver

        if not exists(tgzver):
            #just run was good enough
            sudo('wget %s' % tgzurl, user=parameters.unixuser)
        else:
            pass


        if not exists('html/maintenance'):
            with settings(warn_only=True):

                run('pwd')
                run('ls -tral')
                sudo('tar -zxv -C html --strip-components 1 -f %s' % tgzver, user=parameters.unixuser)
        
        #if not exists('html/.git'):
        #    run('git clone https://gerrit.wikimedia.org/r/p/mediawiki/core.git html')

        with cd('html'):

            if exists('.git'):
                run('git checkout origin/REL1_20')

            with settings(
                user=parameters.unixuser,
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
                user=parameters.unixuser,
                ):

                run('rm -f SMW_setup.php')
                run('rm -f SMW_refreshData.php')
                sudo('ln -s ../extensions/SemanticMediaWiki/maintenance/SMW_setup.php', user=parameters.unixadminuser)
                sudo('ln -s ../extensions/SemanticMediaWiki/maintenance/SMW_refreshData.php', user=parameters.unixadminuser)


def setup_webserver_step2(parameters=None):
    if parameters is None:
        parameters={}

    ALLOW_DESTROY=parameters.destroy
    adict = {
        'installdbuser':parameters.dbadminuser,
        'installdbpass':parameters.dbadminpass,

        'sysop':parameters.sysop,
        'wikiname':parameters.wikiname,
        'userpass':parameters.userpassword,

        'dbname':parameters.dbname,
        'dbuser':parameters.wikiuser,
        'dbserver':hostnameinternal,
        'wikiAdminuser': parameters.wikiAdminuser, 
        'wikiAdminpass': parameters.wikiAdminpass,
        }




    with settings(user=parameters.unixadminuser):
        with cd('/var/www/html/maintenance'):
            if ALLOW_DESTROY:
                sudo('echo "drop database %(dbname)s" | mysql -u %(installdbuser)s' % adict)
                run('rm -f %s' % parameters.localsettingsfile)
            else:
                print "I'm not allowed to overwrite your database or LocalSettings.pgp. try with --destroy"

            if not exists(parameters.localsettingsfile):
                run('php /var/www/html/maintenance/install.php --installdbuser %(wikiAdminuser)s --installdbpass "%(wikiAdminpass)s" --scriptpath / --dbuser %(dbuser)s --pass "%(userpass)s" --dbtype mysql --dbserver %(dbserver)s --dbname %(dbname)s  %(wikiname)s %(sysop)s' % adict)

        print "updating %s" % parameters.localsettingsfile
        put_text_to_file(localsettingstext, parameters.localsettingsfile)




    with cd('/var/www/html/maintenance'):
        if exists(parameters.localsettingsfile):
            run('php update.php --quick')

    run('apachectl restart')







def setup_bots(parameters=None):
    if parameters is None:
        parameters={}

    with settings(warn_only=True):

        sudo('yum -y install git cpan perl-JSON make subversion')
        sudo('curl -L http://cpanmin.us | perl - MediaWiki::API')

    with settings(warn_only=True):

        sudo('yum -y install gcc autoconf gmp gmp-devel gmp-static python-devel python-crypto gcc python-setuptools')
        sudo('easy_install pip')
        sudo('pip install argparse')
        sudo('pip install fabric')

    with settings(warn_only=True):
        sudo('yum -y install rubygems')
        sudo('gem install rest-client')
        sudo('gem install activesupport')





def main(argv=[]):
    parameters = smwinstaller.loadParameters(argv)
    init(parameters)
    if parameters.debug:
        print parameters
    try:

        if parameters.local:
            localize()


        setup_mysql(parameters)
        setup_php()
        setup_httpd()
        setup_wiki(parameters)
        setup_webserver_step2(parameters)
        setup_bots(parameters)
    except Exception, e:
        traceback.print_exc()                                                                                                                                                            
        print "Exception: %s" % e
        traceback.print_stack()

    host = getpublichostname()
    print 'mysql: %s : %s' % (parameters.wikiAdminuser, parameters.wikiAdminpass)
    print 'wiki: %s : %s' % (parameters.sysop, parameters.userpassword)
    print 'url: http://%s ' % host 



if __name__ == '__main__':

    main(sys.argv)
