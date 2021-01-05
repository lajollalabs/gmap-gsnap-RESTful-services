from settings import IDFILE
from tempfile import *
import subprocess

IDF_VAL  = open ( IDFILE ).read().strip()

class GSNAP: 
        def runGSNAPOnOligo (self, sequence ):
            m1 = self.runGSNAP (sequence)


            i=0
            l=[]
	    
            
            l.append ( m1 )
            for c in sequence:
                rnabuldge = sequence[:i] + '-' + sequence[i+1:]
                m2 = self.runGSNAP ( rnabuldge )
                l.append ( m2 )
                i=i+1
            l = l + (self.runGSNAPWithMismatch ( sequence ))
            return l	
        def runGSNAPWithMismatch ( self, sequence ):
            l = []
            l = l +( self.single_mismatch( sequence, 'A' ) )
            l = l + ( self.single_mismatch ( sequence, 'C' ) )
            l = l + ( self.single_mismatch ( sequence, 'G' ) )
            l = l + ( self.single_mismatch ( sequence, 'T' ) )
            return l
        
        def single_mismatch (self, sequence, substitution_base ):
            i = 0
            l=[]
            for c in sequence:
                newsequence = sequence[:i] + substitution_base + sequence[i+1:]
                m = self.runGSNAP ( newsequence, 'mismatch sub ' + substitution_base + ' at ' + str(i) )
                l.append ( m )
                i=i+1
                return l	
            
            
        def runGSNAP (self, sequence, comment=None ):
            fp = NamedTemporaryFile(mode = "w", suffix='.fa', delete=False)
            with fp as f:
                f.write ( '> seq: \n')
                f.write ( sequence )
                f.write ( '\n')
                f.flush()
            print (fp.name, ' <--- INPUT FILE  ') 
            fo = NamedTemporaryFile(mode='r', suffix='.out', delete=False)
            ss = subprocess.check_call (['gsnap', '-d', IDF_VAL, '-n', '10000', '-o', fo.name, fp.name])
            print (' ------- ')	
            res = fo.read ()
            if comment is not None:
                res = 'comment:'+comment+'\n' + res
            res = 'input-sequence:'+sequence+'\n' + res
            
            return res
