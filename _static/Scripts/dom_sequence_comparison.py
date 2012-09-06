### Test script to show off some of the functionality of codebase ###
import sys
from time import time

sys.path.append('/home/glue/Dropbox/pyrecords')
from Utilities.utils import to_dic, from_file, histogram  #From pyrecords

sys.path.append('../DataTypes')
from cdd_fields import domain_manager  #Handles all domain data I/O

sys.path.append('../CDUtilities')
from cd_utils import formatted_domains, network_diagram, domain_translator, network_outfile, from_cdd_file, crop_accession
from seq_utils import protein_file, assign_dom_seq


if __name__ == '__main__':	
    domains=list(from_cdd_file(domain_manager, 'TestData/TestSet.txt', warning=False))  #CAUSING AN ERROR!!!
    proteins=protein_file('../CDUtilities/whl22.v1.0.orf.fasta')
    domains=crop_accession(domains)
    assign_dom_seq(domains, proteins)
    
    
