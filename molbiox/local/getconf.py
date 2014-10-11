
import os

MBXdname = '.molbiox'

def getMBXpath(path=None):
    "Find the `.molbiox` for `path`"
    if not path:
        path = os.getcwd()

    while True:
        mbxpath = os.path.join(path, MBXdname)
        if os.path.isdir(mbxpath):
            return mbxpath
        path_ = os.path.split(path)[0]
        if path == path_:
            raise MolbioxDirNotFound
        else:
            path = path_



