from os import remove, listdir, getcwd, path
from urllib import urlretrieve
from zipfile import ZipFile
from shutil import rmtree, move

print "Getting latest version"
urlretrieve("https://github.com/parrottq/TerraServer/archive/Update.zip", "zipped.zip")

print "Extracting"
with ZipFile(open("zipped.zip", 'rb')) as zipper:
    zipper.extractall("")

remove("zipped.zip")

print "Removing old files"
listoffiles = listdir(getcwd())
listoffiles.remove("TerraServer-Update")
listoffiles.remove("start.py")
try:
    listoffiles.remove("TerrariaServer.exe")
    listoffiles.remove(".git")
except ValueError:
    pass
for e in listoffiles:
    if path.isdir(e):
        rmtree(e)
    else:
        remove(e)

print "Replacing with new files"
listofupdates = listdir("TerraServer-Update")
listofupdates.remove("start.py")
for e in listofupdates:
    try:
        move("TerraServer-Update\\" + e, getcwd())
    except Exception:
        pass

import main
