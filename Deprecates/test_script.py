### Test script to show off some of the functionality of codebase ###
from time import time
from utils import to_dic, from_file
from cdd_domains import domain_manager

if __name__ == '__main__':	
    start=time()
    domains=from_file(domain_manager, 'FullSeaUrchin.txt')  #.15 seconds for this, about 6 seconds for full file
    domains=to_dic(domains)
    print 'It took str(time()-start) seconds to read in str(len(domains)) sea urchin domains and assign unique\
          dictionary keys'
    ### add some domains from scratch ###
    domains['fake entry']=domain_manager.dict_make(Query='Fake Query')
    print domains['fake entry']
#    strictnamedtuple('hi')
#    d0=DomainCDD()
#    d1=DomainCDD(Query='steve', Start=20.0)
#    d2=DomainCDD(Query='bo', Start=8.0)
#    d3=DomainCDD(Query='gay', Start=50.0)
#    print dir(d1), d1
#    ds=(d1,d2,d3)
#    dic=ManagerCDD()
#    for d in ds:
#        dic[d.get_uniquekey()]=d
#    domains=from_file('TestSet.txt')
#    print len(domains)
#    dfile=to_dic(domains)
#    fd=formatted_domains(dfile)
#    a=network_diagram(fd, 'cl09099')
#    network_outfile(a, 'junknetwork', summary=True, adjacency=True)
#    Pixel = namedtuple('DomainCDD', DomainCDD._fields + 'FagField')
#    p=Pixel()
#    print p    
    
    
