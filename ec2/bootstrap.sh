#!/bin/env bash

sudo yum -y install git gcc autoconf gmp gmp-devel gmp-static python-devel python-crypto gcc 
sudo easy_install pip
sudo pip install argparse
sudo pip install fabric

git clone git://github.com/cariaso/smwcon2012bots.git
cd smwcon2012bots/ec2
./install-semantic-mediawiki.py --debug

exit;


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

