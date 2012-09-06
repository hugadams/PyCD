### Methods in particluar to making custom domain analysis.  Not general, core methods. ###

sys.path.append('/home/glue/Dropbox/pyrecords')
from Utilities.utils import sortbyarg  #From pyrecords

from operator import attrgetter
from itertools import ifilter
from collections import namedtuple

def formatted_domains(domains, style='Domain Accession'):
    ''' Keys QueryAccessions to their domains ie: 'xp2343242.2 : cl002343, cl002343, cl202032.  This requires sorting to
        retain the domains in their positional order.  If a dictionary is passed, sorting is done automatically.  If 
        an interable is passed, program assumes it is correctly sorted from the sortbyarg utility.
        
        style:  kw that determines if domains will be in their CD accession (eg cl02342) or shortname (Clectin)
                exact style kws are 'Domain Accession' or 'Domain Shortname.
	WAR'''
     #If domains is dictionary, presort.  Otherwise, assume user as already passed a the return of sortbyarg
    if type(domains) == dict:
        domains=sortbyarg(domains, 'Accession', 'Start')  #Sorting is still suceptible to string sorting issues
 
    if style=='Domain Accession':
        fget=attrgetter('DomAccession')
    elif style=='Domain Shortname':
        fget=attrgetter('DomShortname')
    else:
        raise KeyError('style parameter must be Domain Accession or Domain Shortname')
    
    fdic={}
    for dom in domains:
        if dom.Accession not in fdic.keys():
            fdic[dom.Accession]=[]
        fdic[dom.Accession].append(fget(dom))
    return fdic

def histogram(cd_dic, *fields):
    ''' Returns count of unique occurrences for a field in CDDomain record.  Literally it is counting the
    occurrences of a unique attribute.  In practice, this is useful for understanding the domain distribution
    in the dataset.  Build to take in multple fields for flexibility.'''
    out={}
    for k, valuelist in get_fields(cd_dic, *fields).items():
        unique=list(set(valuelist))
        out[k]=tuple([(v, valuelist.count(v)) for v in unique])
    return out   
def overlap(domains):
    ''' Incomplete'''
    if type(domains) == dict:
        domains=sortbyarg(domains, 'Accession', 'Start')  #Sorting is still suceptible to string sorting issues
    raise NotImplementedError

def singles_mosaics(formatted_domains_dic):
    ''' Returns all formatted domains that are merely single domains or multidomains (mosaics).
        Could be interfaced directly to cd_dic, but figured it would be better to pass formatted
        domains directly.  Domain name style determined by formatted_domains_dic'''
    singles={} ; mosaics = {}
    for (k,v) in formatted_domains_dic.items():
        if len(v) > 1:
            mosaics[k]=v
        else:
            singles[k]=v
    return (singles, mosaics)

def network_diagram(formatted_domains_dic, domain, **kwargs):
    ''' Creates a network diagram from formatted_domains_dic with central node as "domain". These accept dictionaries of the return of the
    singles_mosaics() method.  If they are not passed, the program will run this method on the formatted_dom_dic.'
    Domain name style determined by formatted_domains_dic'''
    left_domains=[] ; right_domains=[]
    doubles=0 ; Ncount=0 ; Ccount=0 ; sings=0

    ### See if user wants to switch the style to accession

    ### Get singles/mosaics either from file or from formatted_domains_dic and sintles_mosaics() method ###
    singles=kwargs.pop('singles', None)
    mosaics=kwargs.pop('mosaics', None)
    if type(singles) != dict and type(singles) != dict: #If singles and mosaics both not passed
        singles, mosaics = singles_mosaics(formatted_domains_dic)
    
    sings=len( filter(lambda x: x[0]==domain, singles.values() ) )  #If value is == domain
    for (k,v) in mosaics.items():
        if v[0] == domain:
            Ncount += 1
            if v[1] != domain:
                right_domains.append(v[1])
            else:
                doubles += 1
            
        if v[-1] == domain:
            Ccount += 1
            if v[-2] != domain:
                left_domains.append(v[-2])   #Does not update doubles as this would double count!
        
        for dom in v[1:-1]: #Iterate over middle
            dom_ind=v.index(dom)
            domleft=v[dom_ind - 1 ]
            domright=v[dom_ind + 1]
            if dom == domain:
                if domleft != domain and domright != domain:   #A-X-A  for X being domain of interest
                    left_domains.append(domleft)
                    right_domains.append(domright)
                            
                elif domleft != domain and domright == domain:  #A-X-X
                    left_domains.append(domleft)   
                    doubles += 1
                
                elif domleft == domain and domright != domain:  #X-X-A
                    right_domains.append(domright)  #Doubles not up-counted to avoid double counts
                
                elif domleft == domain and domright == domain:  #X-X-X
                    doubles += 1
	#Counting should work right if you left the top 3 if statements act on a long string A-L-L-L-L-B, it should be consistent			
    Network=namedtuple('Network', 'seed_domain, flank_left, flank_right, singles, doubles, n_terminal, c_terminal', verbose=False)
    return Network._make([domain, tuple(left_domains), tuple(right_domains), sings, doubles, Ncount, Ccount])

def network_outfile(network, outstring, delimiter='\t', summary=True, adjacency=True):
    ''' Takes in network object from network_diagram method and outputs it as a summary and/or adjacency.
    For now these are written into the same file.'''
    f=open('outstring', 'w')
    allflanks=list(set(network.flank_left + network.flank_right))  #All unique right/left flanks
    if summary ==True:
	seed=network.seed_domain
	sum_header=delimiter.join([('#Left Flank'), 'Count', 'Right Flank', 'Count', 'Left/Right Disparity' ]) + '\n'
	f.write(sum_header)
	for domain in allflanks:
	    lcount=network.flank_left.count(domain) ; rcount=network.flank_right.count(domain)
	    f.write(('%s_X %s %d %s X_%s %s %d %s %d \n') % \
	          (domain, delimiter, lcount, delimiter, domain, delimiter, rcount, delimiter, abs(rcount - lcount))  )

    if adjacency==True:
	f.write('\n#### Adjacency Matrix ####\n')
	f.write(delimiter + domain+'\n')
	for domain in allflanks:
	    count=network.flank_left.count(domain) + network.flank_right.count(domain)
	    print count, 'here', domain, delimiter
	    f.write(('%s %s %d \n' ) % (domain, delimiter, count))

    f.close()
