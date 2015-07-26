from os import system, remove
from urllib import urlretrieve
from zipfile import ZipFile
from shutil import rmtree, move

#with open("zipped.zip", 'w') as zipfile:
#    zipfile.write(urlopen("https://github.com/parrottq/TerraServer/archive/Update.zip").read())

urlretrieve("https://github.com/parrottq/TerraServer/archive/Update.zip", "zipped.zip")

with ZipFile(open("zipped.zip", 'rb')) as zipper:
    zipper.extractall("")

remove("zipped.zip")

remove("TerraServer-Update\\start.py")

move("TerraServer-Update", "")

# rmtree("TerraServer-Update/", True)
