#!/bin/env bash


# wget -O - https://raw.github.com/cariaso/smwcon2012bots/master/ec2/bootstrap.sh | bash


sudo yum -y install git cpan perl-JSON make rubygems subversion python-setuptools
sudo gem install rest-client
sudo gem install activesupport
curl -L http://cpanmin.us | sudo perl - MediaWiki::API



sudo easy_install pip
sudo pip install argparse
sudo yum -y install gcc autoconf gmp gmp-devel gmp-static python-devel python-crypto gcc
sudo pip install fabric


#exit;
cd ~
git clone git://github.com/cariaso/smwcon2012bots.git

cd smwcon2012bots/ec2
sudo ./install-semantic-mediawiki.py --debug





exit
# Do I need to explain that this is not secure?
# is it ONLY for setting up an ec2 which will live for ~1hr
sed -ibak "s/^#PasswordAuthentication\syes/PasswordAuthentication yes/" /etc/ssh/sshd_config
sed -ibak "s/^PasswordAuthentication\sno/#PasswordAuthentication no/" /etc/ssh/sshd_config
/etc/init.d/sshd restart

export password=`< /dev/urandom tr -dc a-z0-9 | head -c8`
echo -n "creating users "
for i in {1..100}
do
   export username="smwcon$i"
   echo -n "$username " 
   adduser $username > /dev/null 2>/dev/null
   echo -e "$password\n$password" | passwd $username > /dev/null 2> /dev/null
done
echo "."
echo "password is $password"

