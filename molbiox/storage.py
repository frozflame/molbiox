
import gzip
import hashlib
from os.path import join, exists
from molbiox.mbxconf import mbxpath, confdic
from molbiox.mbxconf import BlobIntegrityError

fasta_line_length = confdic['fasta_line_length']

class Blob(object):
    """
    KVStore pure sequences as blobs
    Not suitable for very large sequences; consider split.

    Accept a `bytes` object as argument

        blob = Blob(b'atttcct...tac')
    """

    def __init__(self, content):
        content = content.upper()
        self.address = hashlib.sha1(content).hexdigest()
        self.content = content
    
    @staticmethod
    def blobpath(address): 
        return join(mbxpath, address) + confdic['zipblob']

    def save(self, overwrite=False):
        path = Blob.blobpath(self.address) 
        if not exists(path) or overwrite:
            with gzip.open(path, 'wb') as zipfile:
                zipfile.write(self.content)
            
    @staticmethod
    def load(address):
        path = Blob.blobpath(address)
        with gzip.open(path, 'rb') as zipfile:
            content = zipfile.read()
        blob = Blob(content) 

        # check is mandatory
        if blob.address != address:
            raise BlobIntegrityError(address)
        return blob

    def tofasta(self, filename, mode='wb'):
        with open(filename, mode) as fout:
            fout.write(b'>')
            fout.write(self.address.encode('ascii'))
            fout.write(b'\n')

            start = 0
            while start < len(self.content):
                line = self.content[start: start+fasta_line_length] + b'\n'
                fout.write(line)
                start += fasta_line_length
            

def test_Blob():
    seqdata = b'atgcc' * 100

    # create a blob, and save
    blob = Blob(seqdata)
    blob.save(True)

    print('blob:', blob.address, blob.content)
    blob.tofasta('test/test_Blob_tofasta.fa', 'ab')

    # allow tester / user to modify the blob file intentionally
    input('Press any key to continue ...')

    # load 
    address = blob.address 
    blob = Blob.load(address)

    print('blob:', blob.address, blob.content)
    blob.tofasta('test/test_Blob_tofasta.fa', 'ab')

if __name__ == "__main__":
    test_Blob() 

