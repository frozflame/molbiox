
import os

mbxconf = {
    'dirname': '.molbiox',
    'extblob': '.mbxblob',
    'fasta_line_length': 60,

}

class MBXDirNotFound(Exception):
    pass

def getMBXpath(path=None):
    "Find the `.molbiox` for `path`"
    if not path:
        path = os.getcwd()

    while True:
        mbxpath = os.path.join(path, mbxconf['dirname'])
        if os.path.isdir(mbxpath):
            return mbxpath
        path_ = os.path.split(path)[0]
        if path == path_:
            raise MBXDirNotFound
        else:
            path = path_

def initMBXpdir(path=None):
    if not path:
        path = os.getcwd()
    mbxpath = os.path.join(path, mbxconf['dirname'])
    try:
        os.mkdir(mbxpath)
    except FileExistsError:
        if not os.path.isdir(mbxpath):
            raise
    return mbxpath

mbxpath = getMBXpath()
