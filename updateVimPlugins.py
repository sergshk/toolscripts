#!/usr/bin/env python3

# This is script which updates plugins in my dotfiles repository
# since I am not using any plugin manager I simply decided to roll
# script which will keep plugins up to date and then another script
# which will install/refresh vimrc

# First of all importing neccesary modules
import subprocess 
import json
import sys
import os

# DEFINE constants
pathToTmp = '/tmp'
confRepo = "https://github.com/sergshk/dotfls.git"
helpText = """Command was executed without any parameters, potential mistake?
    Try using --dry-run or --commit to view and commit changes """
usageText = """Usage: updateVimPlugins.py [ARGS]
    -h, --help      display help text
    -e, --esential  install essential version
    -c, --commit    commit changes
    -v, --verbose   verbose output
    -d, --dry-run   display potential changes"""
scriptName=sys.argv[0]
allArgs = sys.argv[1:]
if len(allArgs) < 1:
    print(helpText)
    print(usageText)
    sys.exit(0)

# By default running full vim install
pathToDotVim = 'dotvim'
pathToConfJson = 'vim_plugins.json'
verboseOut = False

# process arguments
for oneArg in allArgs:
    if oneArg in ("-h","--help"):
        print(usageText)
    elif oneArg in ("-e","--essential"):
        pathToDotVim = 'dotvimessential'
        pathToConfJson = 'vim_essential.json'
    elif oneArg in ("-d","--dry-run"):
        dryRunFlag = True
    elif oneArg in ("-v","--verbose"):
        verboseOut = True

# defining method to install plugins from github or direct download of a zip file
def installPlugin(folderName,method,url,fileName):
    printOutput("Installing <" + folderName + "> pugin using method <" + method + ":" + url + ">")
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
# defining method to print output
def printOutput(outputStr):
    if verboseOut:
        print("+++++:" + outputStr)

# cloning my conf repo into tmp
printOutput("Clonning repository " + confRepo)
#sys.exit(0)
subprocess.call(["git","clone",confRepo],cwd=pathToTmp)
# reading JSON file
with open(pathToTmp+"/dotfls/"+pathToConfJson) as myfile:
    confJson = json.load(myfile)

# Check if folder exist and if not create it or delete content.
if os.path.isdir(pathToTmp + "/" + pathToDotVim):
    printOutput("Clearing folder " + pathToTmp + "/" + pathToDotVim)
    subprocess.call(["rm","-fR",pathToTmp + "/" + pathToDotVim + "/*"])
elif os.path.exists(pathToTmp + pathToDotVim):
    printOutput("Removing file " + pathToTmp + "/" + pathToDotVim)
    os.remove(pathToTmp + "/" + pathToDotVim)
else:
    printOutput("Creating folder " + pathToTmp + "/" + pathToDotVim)
    subprocess.call(["mkdir",pathToDotVim],cwd=pathToTmp)
#  move throug JSON file and install all plugins
for plugin in confJson["plugins"]:
    installPlugin(plugin['name'],plugin['method'],plugin['url'],plugin['filename'])

# TODO add copy of the files and backup of old files
