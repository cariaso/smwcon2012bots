#!/usr/bin/sh

# Do I need to explain that this is not secure?
# is it ONLY for setting up an ec2 which will live for ~1hr


yum -y install git cpan perl-JSON make rubygems subversion
gem install rest-client
gem install activesupport
curl -L http://cpanmin.us | perl - MediaWiki::API

cd ~
git clone git://github.com/cariaso/smwcon2012bots.git



sudo sed -ibak "s/^#PasswordAuthentication\syes/PasswordAuthentication yes/" /etc/ssh/sshd_config
sudo sed -ibak "s/^PasswordAuthentication\sno/#PasswordAuthentication no/" /etc/ssh/sshd_config
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

