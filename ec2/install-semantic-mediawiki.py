#!/usr/bin/env python
#License = http://en.wikipedia.org/wiki/WTFPL

import os.path
import sys
import os
import errno
import random
import string
import traceback
import getpass

import smwinstaller

import socket
import httplib
import re

def getsetting(name, default=None):
    try:
        result = run("wget --tries=1 -T1 -O - http://169.254.169.254/latest/meta-data/%s 2> /dev/null" % name)
    except:
        result = default
    return result

def getpublichostname():
    aname = getsetting('public-hostname', env.host)
    if aname:
        return aname
    else:
        return 'localhost'

def getinternalhostname():
    return getsetting('local-hostname', 'localhost')

def getip():
    return getsetting('local-ipv4', '127.0.0.1')


#################################################################

def loadtemplate(templatefn):
    fh = file(templatefn, 'r')
    text = fh.read()
    fh.close()
    return text


try:
    from fabric.api import run, put, cd, lcd, env, get, sudo, settings
    from fabric.contrib.files import exists, append, contains
    from fabric.operations import local
    import fabric
except ImportError:
    print 'without fabric this program is a very limited. try "pip install fabric"'
    # seems silly, but I think --local mode could be made to work fine without it


def init(parameters):

    if parameters.local:
        localize()

    if parameters.remote:
            from urlparse import urlparse
            parsed = urlparse('http://%s' % parameters.remote)
            if parsed.username:
                env.user = parsed.username
                if parameters.unixuser is None:
                    parameters.unixuser = parsed.username
                if parameters.unixadminuser is None:
                    parameters.unixadminuser = parsed.username

            if parsed.password:
                env.password = parsed.password
            if parsed.hostname:
                env.host_string = parsed.hostname
                env.host = parsed.hostname
                env.hosts = [parsed.hostname]
            if parsed.port:
                env.port = parsed.port

            print env

    parameters.publichostname = getpublichostname()
    parameters.hostnameinternal = getinternalhostname()
    parameters.hostip = getip()
    
    if parameters.userpassword is None:
        parameters.userpassword =''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        
    if parameters.wikiAdminpass is None:
        parameters.wikiAdminpass =''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        

    if parameters.unixuser is None:
        parameters.unixuser = getpass.getuser()
    if parameters.unixadminuser is None:
        parameters.unixadminuser = getpass.getuser()

    if parameters.templatedir is None:
        executabledir = os.path.dirname(sys.argv[0])
        parameters.templatedir = os.path.join(executabledir, 'templates')


    print '= template =',parameters.templatedir
    print '= user     =',parameters.unixuser
    print '= sudo     =',parameters.unixadminuser
    print '= public   =',parameters.publichostname
    print '= internal =',parameters.hostnameinternal
    print '= ip       =',parameters.hostip


    print 'Are you sure?',
    if not parameters.yes:
        response = raw_input('y/N ')
        if 'y' in response.lower():
            pass
        else:
            sys.exit()

    adict = {
        'host': parameters.hostnameinternal,
        'hostip': parameters.hostip,
        'userpassword': parameters.userpassword,
        'dbserver': parameters.hostnameinternal,
        'dbhost': parameters.hostnameinternal,
        'dbname': parameters.dbname,
        'wikiuser': parameters.wikiuser,
        'dbadminpass': parameters.dbadminpass,
        'dbadminuser': parameters.dbadminuser,

        'wikiAdminuser': parameters.wikiAdminuser,
        'wikiAdminpass': parameters.wikiAdminpass,
        'hostname': parameters.publichostname,
        'email': parameters.email,
        'wikiname': parameters.wikiname,
    }
    #print adict

    semsettingstemplatefn = os.path.join(parameters.templatedir, 'semanticsettings.template')
    localsettingstemplefn = os.path.join(parameters.templatedir, 'localsettings.template')
    robotstemplatefn      = os.path.join(parameters.templatedir, 'robots.template')

    parameters.semsettingstext   = loadtemplate(semsettingstemplatefn) % adict
    parameters.localsettingstext = loadtemplate(localsettingstemplefn) % adict
    parameters.robotstext        = loadtemplate(robotstemplatefn) % adict

    parameters.apacheconftext = ''


def put_text_to_file(text, filename):

    atmpfn = 'a_tmp_file'
    f = file(atmpfn, 'w')
    f.write(text)
    f.close()
    try:
        put(atmpfn, filename)
    except:
        remotefn = 'a_tmp2_file'
        sudo('chown %s:%s %s' % (parameters.unixuser,
             parameters.unixuser, filename), pty=True)
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

    def sudo(cmd, pty=None, user=None):
        return local(cmd)

    def exists(path):
        return os.path.exists(os.path.join(env.lcwd, path))

    def runlocal(cmd):
        return local(cmd, capture=True)

    run = runlocal
    put_text_to_file = put_text_to_local_file
    cd = lcd


def handle_selinux(parameters=None):

    if exists('/selinux/enforce'):
        print 'SELinux detected'

        active = True
        statusmsg = run('sestatus -v')

        if (re.search('SELinux status:\s+disabled', statusmsg) 
            or re.search('Current mode:\s+permissive', statusmsg)):
            active = False

        if active:
            print 'SELinux is not permissive'

            #allows the wiki to read from the database
            sudo('setsebool -P httpd_can_network_connect=1', pty=True)

            # clobber SE Linux entirely. Hope to be more subtle in time, but this will work for now
            sudo('echo 0 >/selinux/enforce', pty=True)


def setup_mysql(parameters=None):
    if parameters is None:
        parameters = {}

    sudo('yum -y install mysql mysql-server', pty=True)
    sudo('service mysqld restart', pty=True)

    adict = {
        'toadminuser': parameters.dbadminuser,
        'toadminpass': parameters.dbadminpass,
        'todb': parameters.dbname,
        'tohost': parameters.hostnameinternal,

        'wikiusername': parameters.wikiuser,
        'wikiuserpass': parameters.userpassword,
        'hostinternal': parameters.hostnameinternal,
    }

    mysqlcmd = 'mysql -u %(toadminuser)s --password=\'%(toadminpass)s\'' % adict
    adict['mysqlcmd'] = mysqlcmd

    try:
        run('%(mysqlcmd)s -e "create database %(todb)s;"' % adict)
    except:
        print "unable to create the db"

    run('''%(mysqlcmd)s -e "grant index, create, select, insert, update, delete, alter, lock tables on %(todb)s.* to '%(wikiusername)s'@'%(tohost)s' identified by '%(wikiuserpass)s'" ''' % adict)

    adict['toadminuser'] = parameters.wikiAdminuser
    adict['toadminpass'] = parameters.wikiAdminpass

    run('%(mysqlcmd)s -e "GRANT ALL PRIVILEGES ON %(todb)s.* TO \'%(toadminuser)s\'@\'%(tohost)s\' IDENTIFIED BY \'%(toadminpass)s\' with GRANT OPTION;"  ' % adict)


def setup_php(parameters):
    sudo('yum -y install php-devel php-pear php-pecl-apc php php-mysql php-xml', pty=True)


def setup_httpd(parameters):

    sudo('yum -y install httpd httpd-devel', pty=True)

    sudo("perl -p -i.bak -e 's!AddType\s+application/x-httpd-php\s+.php!!' /etc/httpd/conf/httpd.conf", pty=True)
    sudo("perl -p -i.bak -e 's!(AddType\s+application/x-tar\s+\.tgz)!$1\\nAddType application/x-httpd-php .php!' /etc/httpd/conf/httpd.conf", pty=True)

    sudo("perl -p -i.bak -e 's!^DirectoryIndex.*!DirectoryIndex index.html index.php!' /etc/httpd/conf/httpd.conf", pty=True)

    if parameters.apacheconftext:
        if not exists('/etc/httpd/conf.d'):
            sudo('mkdir -p /etc/httpd/conf.d', pty=True)

        localname = '/tmp/httpd-conf-semanticmediawiki.conf'
        put_text_to_file(parameters.apacheconftext, localname)

        try:
            sudo('mv %s /etc/httpd/conf.d/semanticmediawiki.conf' %
                 localname, pty=True)
        except:
            pass


def setup_wiki(parameters=None):
    if parameters is None:
        parameters = {}

    if not exists('/var/www'):
        sudo('mkdir -p /var/www')
    sudo('chown %s:%s /var/www' % (parameters.unixuser, parameters.unixuser), pty=True)

    if not exists('/var/www/html'):
        sudo('mkdir -p /var/www/html')
        sudo('chown %s:%s /var/www/html' % (parameters.unixuser, parameters.unixuser), pty=True)

    if exists('/var/lib/php/session'):
        sudo('chmod a+rwx /var/lib/php/session')

    sudo('yum -y install subversion git')

    with cd('/var/www'):
        sudo('chown %s:%s html' % (parameters.unixuser,
             parameters.unixuser), pty=True)

        tgzver = 'mediawiki-1.20.2.tar.gz'
        tgzurl = 'http://download.wikimedia.org/mediawiki/1.20/%s' % tgzver

        if not exists(tgzver):
            #just run was good enough
            sudo('wget %s' % tgzurl, user=parameters.unixuser)
        else:
            pass

        if not exists('html/maintenance'):
            with settings(warn_only=True):

                sudo('tar -zxv -C html --strip-components 1 -f %s' %
                     tgzver, user=parameters.unixuser)

        #if not exists('html/.git'):
        #    run('git clone https://gerrit.wikimedia.org/r/p/mediawiki/core.git html')

        with cd('html'):

            if exists('.git'):
                run('git checkout origin/REL1_20')

            with settings(
                user=parameters.unixuser,
                ):

                put_text_to_file(parameters.robotstext, '/var/www/html/robots.txt')
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

                        # not working for me
                        'SemanticBundle',
                        
                        # so still relying on these
                        'SemanticForms',
                        'SemanticDrilldown',
                        'SemanticResultFormats',
                        #'SemanticInternalObjects',

                        'ConfirmEdit',
                        'ParserFunctions',
                        'Validator',
                        'DataValues',
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
                    put_text_to_file(parameters.semsettingstext, semsettingsname)

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
        parameters = {}

    ALLOW_DESTROY = parameters.destroy
    adict = {
        'installdbuser': parameters.dbadminuser,
        'installdbpass': parameters.dbadminpass,

        'sysop': parameters.sysop,
        'wikiname': parameters.wikiname,
        'userpass': parameters.userpassword,

        'dbname': parameters.dbname,
        'dbuser': parameters.wikiuser,
        'dbserver': parameters.hostnameinternal,
        'wikiAdminuser': parameters.wikiAdminuser,
        'wikiAdminpass': parameters.wikiAdminpass,
    }

    with settings(user=parameters.unixadminuser):
        with cd('/var/www/html/maintenance'):
            if ALLOW_DESTROY:
                sudo('mysql -u %(installdbuser)s -e "drop database %(dbname)s"' % adict)
                run('rm -f %s' % parameters.localsettingsfile)
            else:
                print "I'm not allowed to overwrite your database or LocalSettings.pgp. try with --destroy"

            if not exists(parameters.localsettingsfile):
                run('php /var/www/html/maintenance/install.php --installdbuser %(wikiAdminuser)s --installdbpass "%(wikiAdminpass)s" --scriptpath / --dbuser %(dbuser)s --pass "%(userpass)s" --dbtype mysql --dbserver %(dbserver)s --dbname %(dbname)s  %(wikiname)s %(sysop)s' % adict)

        print "updating %s" % parameters.localsettingsfile
        put_text_to_file(parameters.localsettingstext, parameters.localsettingsfile)

    with cd('/var/www/html/maintenance'):
        if exists(parameters.localsettingsfile):
            run('php update.php --quick')

    sudo('apachectl restart')

    with settings(warn_only=True):
        sudo('/etc/init.d/iptables stop')


def setup_bots(parameters=None):
    if parameters is None:
        parameters = {}

    with settings(warn_only=True):

        sudo('yum -y install git cpan perl-JSON make subversion')
        sudo('curl -L http://cpanmin.us | perl - --force --notest MediaWiki::API')
        sudo('curl -L http://cpanmin.us | perl - --force --notest MediaWiki::Bot')
        sudo('curl -L http://cpanmin.us | perl - --force --notest LWP::Simple')
        # remove the duplicate downloads with a temp file or a local install?
        #curl -L http://cpanmin.us | perl - --self-upgrade --sudo

    with settings(warn_only=True):

        sudo('yum -y install gcc autoconf gmp gmp-devel gmp-static python-devel python-crypto gcc python-setuptools')
        sudo('easy_install pip')
        sudo('pip install argparse')
        sudo('pip install fabric')


def main(argv=[]):
    parameters = smwinstaller.loadParameters(argv)
    init(parameters)
    if parameters.debug:
        
        print parameters
        handle_selinux(parameters)
        setup_bots(parameters)
        sys.exit()

    try:
        setup_mysql(parameters)
        setup_php(parameters)
        setup_httpd(parameters)
        handle_selinux(parameters)
        setup_wiki(parameters)
        setup_webserver_step2(parameters)
        setup_bots(parameters)

    except Exception, e:
        traceback.print_exc()
        print "Exception: %s" % e
        traceback.print_stack()

    sudo('apachectl restart')

    print 'mysql: %s : %s'  % (parameters.wikiAdminuser, parameters.wikiAdminpass)
    print 'wiki: %s : %s'   % (parameters.sysop, parameters.userpassword)
    print 'url: http://%s ' % parameters.publichostname


if __name__ == '__main__':

    main(sys.argv)
