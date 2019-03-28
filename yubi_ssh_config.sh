#!/bin/bash

# Copyright (c) 2019 Sergey Shkundaleu (http://sergey.iontec.co). All rights reserved.
# This code is licensed under the MIT License (MIT).
# THIS CODE IS PROVIDED *AS IS* WITHOUT WARRANTY OF
# ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING ANY
# IMPLIED WARRANTIES OF FITNESS FOR A PARTICULAR
# PURPOSE, MERCHANTABILITY, OR NON-INFRINGEMENT.

# Checking version of GPG
PACKAGES="gpg gpg-agent pcscd scdaemon"
GPG_COMMAND="gpg" 
echo "INFO Checking GPG version."
VERSION=`gpg --version`
if [ ! -z "${VERSION// }" ]; then
	# GPG installed making sure that version is 2
	VERSION=`echo $VERSION | grep "2\.[0-9].*\.[0-9].*"` 
	if [ -z "${VERSION// }" ]; then
		# Version 1.x installed attempting to correct that but throwing warning
		echo "WARNING This script is designed to work with Ubuntu 18.04"
		echo "WARNING Your gpg version is 1.x script will attempt to install gpg2"
		PACKAGES="gpg2 gpg-agent pcscd scdaemon"
		GPG_COMMAND="gpg2"
	fi
fi
# Installing necessary packages
echo "INFO Installing necessary packages."
sudo apt-get install $PACKAGES
echo "INFO Listing known keys."
# This suppose to create .gnupg folder
$GPG_COMMAND --list-keys
if [ ! -d ~/.gnupg ]; then
	# Our attempt to initiate GPG failed, pan B is to restart
	echo "ERROR .gnupg folder not found"
	echo "ERROR Please try to restart you system and retry running script again"
	exit 1
fi
echo "INFO Backup config files."
# Backup old config files so that user can recover manually
if [ -f ~/.gnupg/gpg.conf ]; then
	echo "INFO Found gpg.conf"
	echo "INFO Making a backup copy into gpg.conf.bak and creating new config"
	mv ~/.gnupg/gpg.conf ~/.gnupg/gpg.conf.bak
fi
if [ -f ~/.gnupg/gpg-agent.conf ]; then
	echo "INFO Found gpg-agent.conf"
	echo "INFO Making a backup copy into gpg-agent.conf.bak and creating new config"
	mv ~/.gnupg/gpg.conf ~/.gnupg/gpg.conf.bak
fi
# Create new config file for gpg
echo "INFO Creating new config files."
# This section is personal and config options is my personal preference (Sergey Sh)
echo "default-preference-list SHA512 SHA384 SHA256 SHA224 AES256 AES192 AES CAST5 ZLIB BZIP2 ZIP Uncompressed" >> ~/.gnupg/gpg.conf
echo "cert-digest-algo SHA512" >> ~/.gnupg/gpg.conf
echo "s2k-digest-algo SHA512" >> ~/.gnupg/gpg.conf
echo "s2k-cipher-algo AES256" >> ~/.gnupg/gpg.conf
echo "no-emit-version" >> ~/.gnupg/gpg.conf
echo "keyid-format 0xlong" >> ~/.gnupg/gpg.conf
echo "list-options show-uid-validity" >> ~/.gnupg/gpg.conf
echo "verify-options show-uid-validity" >> ~/.gnupg/gpg.conf
echo "with-fingerprint" >> ~/.gnupg/gpg.conf
echo "use-agent" >> ~/.gnupg/gpg.conf
# Creating new config file for gpg-agent
# This section is personal and config options is my personal preference (Sergey Sh)
echo "enable-ssh-support" >> ~/.gnupg/gpg-agent.conf
echo "pinentry-program /usr/bin/pinentry-gnome3" >> ~/.gnupg/gpg-agent.conf
echo "default-cache-ttl 60" >> ~/.gnupg/gpg-agent.conf
echo "max-cache-ttl 120" >> ~/.gnupg/gpg-agent.conf
# Identify if gpg-agent already running and find out variable value
GPG_AGEN_ACTIVE=`export | grep GPG_AGENT_INFO`
echo "INFO Checking if gpg-agent is running."
if [ ! -z "${GPG_AGEN_ACTIVE// }" ]; then
	# Agent already potentially running 
	# Check if gpg agent already accepting ssh connections
	if [ -z `gpgconf --list-dirs agent-ssh-socket` ]; then
		# For some reason GPG agent does not provide SSH socket 
		# Goal here is to kill all gpg agents and invoke a clear one which will read new conf file
		echo "WARNING gpg-agent does not have ssh socket"
		echo "WARNING Because of that we will kill all agents"
		echo "WARNING And start fresh one with config we just created"
		sudo killall gpg-agent
		eval $(gpg-agent --daemon --enable-ssh-support)
	fi
	echo "INFO Making backup copy of .bashrc."
	# Making backup copy of .bashrc
	if [ -f ~/.bashrc ]; then
		cp ~/.bashrc ~/.bashrc.bak
	fi
	echo "INFO Updating .bashrc."
	# Writing auto socket detection into config file
	echo 'export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)' >> ~/.bashrc
else
	# Since we can't find GPG_AGENT_INFO then we need to put GPG agent initiation into bashrc
	echo "ERROR GPG_AGENT_INFO environment variable was not found"
	echo "ERROR That means gpg-agent invocation has to be placed into .bashrc"
	echo "ERROR This particular script was not designed for such situation"
	echo "ERROR However we will attempt to create invocation in .bashrc"
	echo "ERROR Backup of your original .bashrc coudl be found in .bashrc.bak"
	echo "ERROR In case thing does not work out please recover from backup"
	echo "INFO Making backup copy of .bashrc."
	# Making backup copy of .bashrc
	if [ -f ~/.bashrc ]; then
		cp ~/.bashrc ~/.bashrc.bak
	fi
	echo "INFO Attempting to ingest gpg-agent initiation into .bashrc."
	echo 'eval $(gpg-agent --daemon --enable-ssh-support)' >> ~/.bashrc
	echo 'export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)' >> ~/.bashrc
fi
# Check is GPG COMMAND was gpg2 then inject alias for the future reference.
if [ $GPG_COMMAND -e "gpg2" ]; then
	# Adding alias
	echo "WARNING Creating alias for gpg2"
	echo "alias gpg='gpg2'" >> ~/.bash_aliases
fi
