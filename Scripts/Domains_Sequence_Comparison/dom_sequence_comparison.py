### Test script to show off some of the functionality of codebase ###
import sys
from time import time

sys.path.append('/home/glue/Dropbox/pyrecords')
from Utilities.utils import to_dic, from_file, histogram  #From pyrecords

sys.path.append('../../DataTypes')
from cdd_fields import domain_manager  #Handles all domain data I/O

sys.path.append('../../CDUtilities')
from cddutils import formatted_domains, network_diagram, network_outfile, from_cdd_file, crop_accession
from seq_utils import proteins_from_file, assign_dom_seq


if __name__ == '__main__':	
 
    domains_file='../../TestData/TestSet.txt'  #In test data directory
    proteins_file='../../TestData/whl22.v1.0.orf.fasta'
    
    domains=list(from_cdd_file(domain_manager, domains_file)) 
    proteins=proteins_from_file(proteins_file)
    domains=crop_accession(domains)
    domains=assign_dom_seq(domains, proteins)
    print domains
    
