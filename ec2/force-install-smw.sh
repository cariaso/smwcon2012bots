#!/bin/env bash

sudo yum -y install git gcc autoconf gmp gmp-devel gmp-static python-devel python-crypto gcc python-setuptools subversion
sudo easy_install pip
sudo pip install argparse
sudo pip install fabric

git clone git://github.com/cariaso/smwcon2012bots.git
cd smwcon2012bots/ec2
./install-semantic-mediawiki.py --yes --local $@

