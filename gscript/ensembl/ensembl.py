from tempfile import *
import subprocess
import pathlib



IDF_VAL  = open ('/data/bedtools-ptr').read().strip()

class ENSEMBL: 
    def get_sequence(self,chrom, chromStart, chromEnd, name="temp", strand="\+", comment=None ):
        fp = NamedTemporaryFile(mode = "w", suffix='.bed', delete=False)
        print ( 'strand ' + strand )
        print ( ' chromStart ', chromStart )
        print ( ' chromEnd', chromEnd )
        print ( 'name ' + name )
        print ( 'chrom ' + chrom )
        with fp as f:
            line = chrom + '\t' + str(chromStart) + '\t' + str(chromEnd) + '\t' + str(name) + '\t1\t' + str(strand)
            print (line)
            f.write (line)
            f.write ( '\n')
            f.flush()
        print (fp.name, ' <--- INPUT FILE  ') 
        fo = NamedTemporaryFile(mode='r', suffix='.out', delete=False)
        #bedtools getfasta -fi Homo_sapiens.GRCh38.dna.primary_assembly.fa -bed test.bed -s
        print ( fo.name )
        ss = subprocess.check_call (['bedtools', 'getfasta', '-fi', IDF_VAL, '-bed', fp.name, '-fo', fo.name])
        print (' ------- ')
        #print (pathlib.Path(fo).parent.absolute())
        print ( fo.name )
        res = fo.read ()
        if comment is not None:
            res = 'comment:'+comment+'\n' + res
            
        print ( res )
        return res
