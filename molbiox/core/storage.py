
import gzip
import hashlib
from os.path import join, exists
from molbiox.local import blobdir

blksize = 65536

class Blob(object):
    def __init__(self, content):
        self.address = hashlib.sha1(content).hexdigest()
        self.content = content
    
    @staticmethod
    def mkpath(address):
        join(blobdir, address[:2], address[2:])
        
    def save(overwrite=False):
        path = Blob.mkpath(self.address)
        if not exists(path) or overwrite:
            with gzip.open(path, 'wb') as zps:
                zps.write(content)
            
    @staticmethod
    def load(address):
        path = Blob.mkpath(address)
        with gzip.open(path, 'rb') as zps:
            content = zps.read()
        blob = Blob(content) 

        if blob.address != address:
            raise BlobCorrupted(address)


