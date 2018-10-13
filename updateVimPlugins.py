#!/usr/bin/env python3

# This is script which updates plugins in my dotfiles repository
# since I am not using any plugin manager I simply decided to roll
# script which will keep plugins up to date and then another script
# which will install/refresh vimrc

# First of all importing neccesary modules
import subprocess 
import json

# DEFINE constants
pathToTmp = '/tmp'
pathToDotVim = 'dotvim'
confRepo = "https://github.com/sergshk/dotfls.git"

# defining method to install plugins from github or direct download of a zip file
def installPlugin(folderName,method,url,fileName):
    if ("git" == method):
        # just cloning repo
        subprocess.call([method,"clone",url],cwd=pathToTmp)
    else:
        # we have to download zip
        # then extract and delete zip file to keep tmp clean
        subprocess.call(["mkdir",folderName],cwd=pathToTmp)
        # download zip into folder we've created above
        subprocess.call([method,"-O",pathToTmp+ "/" + folderName + "/" + fileName,url])
        subprocess.call(["unzip",fileName],cwd=pathToTmp+"/"+folderName)
        # removing craft
        subprocess.call(["rm","-fR",pathToTmp + "/" + folderName + "/" + fileName])
    subprocess.call("cp -r "+pathToTmp+"/"+folderName+"/* "+pathToTmp+"/"+pathToDotVim+"/",shell=True)
    subprocess.call(["rm","-fR",pathToTmp + "/" + folderName])
# cloning my conf repo into tmp
subprocess.call(["git","clone",confRepo],cwd=pathToTmp)
# reading JSON file
with open(pathToTmp+"/dotfls/vim_plugins.json") as myfile:
    confJson = json.load(myfile)

# TODO Check if folder exist and if not create it.
subprocess.call(["mkdir",pathToDotVim],cwd=pathToTmp)
#  move throug JSON file and install all plugins
for plugin in confJson["plugins"]:
    installPlugin(plugin['name'],plugin['method'],plugin['url'],plugin['filename'])

# TODO add copy of the files and backup of old files
