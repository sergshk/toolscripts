#!/usr/bin/env python3

# This is script which updates plugins in my dotfiles repository
# since I am not using any plugin manager I simply decided to roll
# script which will keep plugins up to date and then another script
# which will install/refresh vimrc

# First of all importing neccesary modules
import subprocess 

# DEFINE constants
pathToTmp = '/tmp'
pathToDotVim = 'dotvim'
# various URLs
urltaglist = "https://www.vim.org/scripts/download_script.php?src_id=19574"
urlvcscommand = "https://github.com/vim-scripts/vcscommand.vim.git"
urlnerdtree = "https://github.com/scrooloose/nerdtree.git"
urlsyntastic = "https://github.com/vim-syntastic/syntastic.git"

# TODO Check if folder exist and if not create it.
subprocess.call(["mkdir",pathToDotVim],cwd=pathToTmp)

# TODO Automate this, but for now simply hardcoding each os the 
# installed modules

# MODULE taglist
# this has nto been update for ages https://github.com/vim-scripts/taglist.vim
# as such best way to find is from https://www.vim.org/scripts/script.php?script_id=273
# my taglist onthe latest (4.6) version
# TODO check if taglist folder exist
taglistFolder = "taglist"
taglistFile = "taglist_46.zip"
subprocess.call(["mkdir",taglistFolder],cwd=pathToTmp)
subprocess.call(["wget","-O",pathToTmp+ "/" + taglistFolder + "/" + taglistFile,urltaglist])
subprocess.call(["unzip",taglistFile],cwd=pathToTmp+"/"+taglistFolder)
# deleting zip file to keep vimfolder clean
subprocess.call(["rm","-fR",pathToTmp + "/" + taglistFolder + "/" + taglistFile])
# copy plugin into vimfolder
subprocess.call("cp -r "+pathToTmp+"/"+taglistFolder+"/* "+pathToTmp+"/"+pathToDotVim+"/",shell=True)
# cleanup
subprocess.call(["rm","-fR",pathToTmp + "/" + taglistFolder])

# MODULE vcscommand
# using GitHub repository git clone https://github.com/vim-scripts/vcscommand.vim.git
# clone repo
vcscommandFolder = "vcscommand.vim"
subprocess.call(["git","clone",urlvcscommand],cwd=pathToTmp)
# move files into my repository 
subprocess.call("cp -r "+pathToTmp+"/"+vcscommandFolder+"/* "+pathToTmp+"/"+pathToDotVim+"/",shell=True)
# cleanup
subprocess.call(["rm","-fR",pathToTmp + "/" + vcscommandFolder])

# MODULE NERDTree
# using GitHub repository git clone https://github.com/scrooloose/nerdtree.git
# clone repo
subprocess.call(["git","clone",urlnerdtree],cwd=pathToTmp)
# move files into my repository
nerdtreeFolder = "nerdtree"
subprocess.call("cp -r "+pathToTmp+"/"+nerdtreeFolder+"/* "+pathToTmp+"/"+pathToDotVim+"/",shell=True)
# cleanup
subprocess.call(["rm","-fR",pathToTmp + "/" + nerdtreeFolder])

# MODULE sysntastic 
# clone repo
subprocess.call(["git","clone",urlsyntastic],cwd=pathToTmp)
# move files into my repository
syntasticFolder = "syntastic"
subprocess.call("cp -r "+pathToTmp+"/"+syntasticFolder+"/* "+pathToTmp+"/"+pathToDotVim+"/",shell=True)
# cleanup
subprocess.call(["rm","-fR",pathToTmp + "/" + syntasticFolder])

