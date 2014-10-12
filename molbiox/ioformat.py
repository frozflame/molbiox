
import re
import os

from molbiox.storage import Blob
from molbiox.getconf import mbxconf

fasta_line_length = mbxconf['fasta_line_length']
fasta_read_blksize = 1024

def guessName(fname):
    name = os.path.split(fname)[1]
    name = os.path.splitext(name)[0]
    return name

class FastA(object):
    def __init__(self, fname):
        self.fname = fname  

    def __iter__(self):
        return self.generator()

    def generator(self):
        """
        Iterate through a FastA file, each time yield a dict

            {
                'name': 'orf1234',
                'data': b'ATTCTAD',
            }

        Not suitable for very large sequences
        """
        
        def mkdic(seqname, seqdata):
            if not seqname:
                seqname = 'anonymous'
            return dict(name=seqname, data=seqdata)

        # in case of a pure sequence file
        seqname = ''
        seqdata = b''

        for line in open(self.fname, 'rb'):
            if line.startswith(b'>'):
                
                # previous `seqdata` got data, yield it 
                if seqdata:
                    yield mkdic(seqname, seqdata)
                seqdata = b''
                seqname = line.strip()[1:].decode('ascii')

            else:
                seqdata += line.strip()

        if seqdata:
            yield mkdic(seqname, seqdata)

    def store(self):
        for dic in self:
            blob = Blob(dic['data'])
            blob.save()
            dic['hash'] = blob.address



# quite complex...
def reformatFastA(oldfname, newfname, overwrite=False):
    ifile = open(oldfname, 'rb')
    ofile = open(newfname, 'wb')

   
    datafield = re.compile(b'')
    namefield = re
    block = ofile.read(fasta_read_blksize)
    while block:
        for i in range(len(block)):
            pass 

def test_iterateFastA():
    itfasta = iterateFastA('test/hello.fa')
    for d in itfasta:
        print(d)

if __name__ == "__main__":
    fasta = FastA('test/hello.fa')
    for dic in fasta:
        print(dic)
    fasta.store()

