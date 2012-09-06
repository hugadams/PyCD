from Bio import SeqIO, Seq
from Bio.Alphabet import generic_protein
from operator import itemgetter

### Makes a dictionary keyed by protein id from SeqIO.parse.  Parse returns a tuple with count and seq object
### for example (0, Seq0), (1, Seq1).  We then are taking the second field (Seq) and keying a dictionary by id attribute.

nameget=itemgetter(1)  #This is ID column of SEQ object
proteins=[( nameget(record).id, record) for record \
         in enumerate(SeqIO.parse(open("whl22.v1.0.orf.fasta"), "fasta", generic_protein)) ]


print proteins[0]
