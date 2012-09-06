### Utilities for handling protein sequence data that 
### may or may not already be built into the biopython framework.
### Mostly these are for convienence
from operator import attrgetter
from Bio import SeqIO
from Bio.Alphabet import generic_protein

import sys
sys.path.append('/home/glue/Dropbox/pyrecords')
from Utilities.utils import to_dic  #From pyrecords

### Makes a dictionary keyed by protein id from SeqIO.parse.  Parse returns a tuple with count and seq object
### for example (0, Seq0), (1, Seq1).  We then are taking the second field (Seq) and keying a dictionary by id attribute.

def protein_file(infile, filetype='fasta'):
    ''' Reads in a protein file and returns all seq records as iterable. Easy to key later using
    my records utilities.'''
    return tuple([record[1] for record \
         in enumerate(SeqIO.parse(open(infile), filetype, generic_protein))])  #Method autostrips the '>'


def assign_dom_seq(domains, seqrecords, warning=True):
    '''Method takes in domain iterable as well as sequences and returns subclasses (either mutable or immutable)
       that have a new field.  For now, domains must be a list of domain objects and sequences must be list of
       sequence records.  Comparison is done through the name attribute.  This uses a custom algorithm that is specific
       to sorting.  Basically it works like this:
          step 1: Identify all names that are shared between domains, sequences.
          step 2: Take subset of each domains, sequences in this shared list.
          step 3: Sort both lists by the name argument (because the lists are the same length, this will
                  order them identically)
          step 4: Compare with not direct lookup involved (ie no If i in seq and in domains...)
          Because sets are used, duplicates are ERASED.  
          Warning prints warnings to alert users to cases when domains have accessions not in the sequences list.'''

    acc_get=attrgetter('Accession')

    unique_doms=set([acc_get(dom) for dom in domains])  #Usually duplication in domains record
    seqs=dict((seq.name, seq) for seq in seqrecords if seq.name in unique_doms) #Only extract sequences relevant to domains

    if warning:  #Replace with warnings later
        if len(unique_doms) > len(seqrecords):
            print '\nWARNING: assign_dom_sequnce() recieved %s domains, from %s unique protiens;however,\
            only %s of these were found in the passed sequences.'%(len(unique_doms), len(seqrecords), len(seqs))

    for domain in domains:
        sequence=seqs[acc_get(domain)].seq
        print sequence[domain.Start:domain.End]
        print len(sequence)
   
 #  obj=obj._replace( **{field:newval} )
   
            
        
if __name__ == '__main__':	
    a=to_dic(protein_file('whl22.v1.0.orf.fasta'), 'id')
    print a.items()[0]
