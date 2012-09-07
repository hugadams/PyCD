### Test script to show off some of the functionality of codebase ###
import sys
from time import time

sys.path.append('/home/glue/Dropbox/pyrecords')
from Utilities.utils import to_dic, from_file, histogram  #From pyrecords

sys.path.append('../DataTypes')
from cdd_fields import domain_manager  #Handles all domain data I/O

sys.path.append('../CDUtilities')
from cd_utils import formatted_domains, network_diagram, domain_translator, network_outfile

if __name__ == '__main__':	
    start=time()
  #  domains=from_file(domain_manager, 'TestData/FullSeaUrchin.txt', skip_assignment=True)  
    domains=from_file(domain_manager, 'TestData/TestSet.txt')
    domains=to_dic(domains, 'Accession', 'DomAccession', 'Start', 'End')        
    print 'It took %s seconds to read in %s sea urchin domains and assign unique\
    dictionary keys, totalling %s bytes in memory' % ((time()-start), len(domains), sys.getsizeof(domains))
    print domains.items()[0]

      
    ### add some domains from scratch ###
    print '\nIt is trivially easy to add new entries manually, and field defaults will be assigned for empty\
    fields.  Field typechecking is enforced!'

    domains['fake entry']=domain_manager.dict_make(Query='Fake Query')
    print domains['fake entry']
    domains.pop('fake entry')
    
    print '\nLets cast the domains into a special form'
    fd=formatted_domains(domains)

    print fd.items()[0:3]
    print '\nThese can also be queried by domain shortname rather than accession'

    fd=formatted_domains(domains, style='Domain Shortname')
    print fd.items()[0:3]
    
    print '\nBecause domains have records in terms of accession (eg cl02321) and shortname (eg Clectin) \
    I have a simple function to translate between these'
    keydic=dict( domain_translator(domains) )#Takes list or dictionary input
    print keydic.items()[0:3]
    
    print '\nIts easy to make a histogram to see which domains are the most prolific'
    hist=histogram(domains, 'DomAccession', sorted_return=True)
    print hist['DomAccession'][0:3]

    print '\nI can easily create a network diagram with any domain as the node, but I will use my translator \
    to easily change the name from accession to shortname'
    domain_net=network_diagram(fd, keydic['cl09941'])

    print '\nI will now output this network stuff into a simple outfile called "testnetwork.txt"'
    network_outfile(domain_net, 'testnetwork.txt', summary=True, adjacency=True)

    
    
