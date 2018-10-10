#!/usr/bin/env python3

# This is script which updates plugins in my dotfiles repository
# since I am not using any plugin manager I simply decided to roll
# script which will keep plugins up to date and then another script
# which will install/refresh vimrc

# First of all importing neccesary modules
import subprocess 

# DEFINE constants
pathToRepo = '../dotfiles'
pathToVimFolder = 'dotvim'

# TODO: Automate this, but for now simply hardcoding each os the 
# installed modules

# MODULE taglist
# this has nto been update for ages https://github.com/vim-scripts/taglist.vim
# as such best way to find is from https://www.vim.org/scripts/script.php?script_id=273
# my taglist onthe latest (4.6) version

# MODULE vcscommand
# using GitHub repository git clone https://github.com/vim-scripts/vcscommand.vim.git
# clone repo
subprocess.call(["git","clone","https://github.com/vim-scripts/vcscommand.vim.git"],cwd='/tmp')
# move files into my repository 
subprocess.call("cp /tmp/vcscommand.vim/doc/* ../dotfiles/dotvim/doc/",shell=True)
subprocess.call("cp /tmp/vcscommand.vim/plugin/* ../dotfiles/dotvim/plugin/",shell=True)
subprocess.call("cp /tmp/vcscommand.vim/syntax/* ../dotfiles/dotvim/syntax/",shell=True)

# MODULE NERDTree
# using GitHub repository git clone https://github.com/scrooloose/nerdtree.git
# clone repo
subprocess.call(["git","clone","https://github.com/scrooloose/nerdtree.git"],cwd='/tmp')
# move files into my repository
subprocess.call("cp -r /tmp/nerdtree/autoload/* ../dotfiles/dotvim/autoload/",shell=True)
subprocess.call("cp /tmp/nerdtree/doc/* ../dotfiles/dotvim/doc/",shell=True)
subprocess.call("cp /tmp/nerdtree/plugin/* ../dotfiles/dotvim/plugin/",shell=True)
subprocess.call("cp /tmp/nerdtree/syntax/* ../dotfiles/dotvim/syntax/",shell=True)
subprocess.call("cp -r /tmp/nerdtree/lib/* ../dotfiles/dotvim/lib/",shell=True)
# special folder only for this plugin
# TODO: check if it exist
subprocess.call("cp /tmp/nerdtree/nerdtree_plugin/* ../dotfiles/dotvim/nerdtree_plugin/",shell=True)

