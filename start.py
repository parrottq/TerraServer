from os import system, remove, listdir, getcwd, path
from urllib import urlretrieve
from zipfile import ZipFile
from shutil import rmtree, copy, move

# with open("zipped.zip", 'w') as zipfile:
#    zipfile.write(urlopen("https://github.com/parrottq/TerraServer/archive/Update.zip").read())

urlretrieve("https://github.com/parrottq/TerraServer/archive/Update.zip", "zipped.zip")

with ZipFile(open("zipped.zip", 'rb')) as zipper:
    zipper.extractall("")

remove("zipped.zip")

listoffiles = listdir(getcwd())
listoffiles.remove("TerraServer-Update")
listoffiles.remove("start.py")
for e in listoffiles:
    print e
    if path.isdir(e):
        rmtree(e)
    else:
        remove(e)

listofupdates = listdir("TerraServer-Update")
listofupdates.remove("start.py")
for e in listofupdates:
    try:
        move("TerraServer-Update\\" + e, getcwd())
    except Exception:
        print e

# rmtree("TerraServer-Update/", True)
