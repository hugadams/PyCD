##### Utilities functions for operating on DomainCDD and ManagerCDD classes.
##### Not type checked and argument names are kept intentionally generic to 
##### encourage reuse.
from operator import attrgetter, itemgetter

###### Utilities to operate on a single DomainCDD instance 
### Note, all namedtuple methods are already inherited
### http://docs.python.org/library/collections.html#collections.namedtuple 

####### Utilities designed for ManagerCDD class (not type checked; terminology purposly generic) ###########
def sortbyarg(dic, *valuefields):
    ''' Enter list of fields/attribes to sort by.  For multiple field, will sort
      in order of entry.  All values in dictionary must have attributes corresponding to these fields.
      expects a dictionary of DomainCDD objects but should work in general.'''
    return tuple(sorted(dic.values(), key=attrgetter(*valuefields)))   

def sortbyitem(dic, *indicies):
    ''' Same as above but sorting by index'''
    return tuple(sorted(dic.values(), key=itemgetter(*indicies)))   

def get_field(dic, valuefield):
    ''' Returns all values of a single field/attribue (wrapper for attrgetter) as a tuple'''
    f=attrgetter(valuefield)
    return tuple([f(v) for v in dic.values()])

def get_fields(dic, *valuefields):
    ''' Returns all values of the *fields/attribue in a dictionary, keyed by attrname'''
    out={}
    for vfield in valuefields:
        out[vfield]=get_field(dic, vfield)
    return out
    
def get_subset(dic, *valuefields, **kwargs):
    ''' Returns a new dictionary, with key and value fields defined by user.  There are
        to keyword args to this function (python 2.x doesn't allow variable neght *args and
        fixed keywords...)
        newkey: User can pass a field which will become the newkey to the dictionary.  
                If None, default keys of the original dictionary will be used.
        valuetype: kw to determine how values are contained (tuple, list, DomainsCDD)'''
    newkey=kwargs.pop('newkey', None)
    valuetype=kwargs.pop('valuetype', 'DomainsCDD')  #For now, this is not yet implemented.
    fget=attrgetter(*valuefields)        
    if newkey is None:
        return tuple( (k,fget(v) ) for k,v in dic.items() )  
    kget=attrgetter(newkey)    
    return tuple( (kget(v), fget(v))  for k,v in dic.items() )

def from_file(infile):
    ''' Take in CDD superfamilies file, return a list of DomainCDD objects.  Note, only data
        filter at work is the line length of the stripped/split lines.  This removes both the
        initial comments and the header.  Should improve it later '''
    from cdd_domains import DomainCDD, strict_fields #Leave in here to avoid recursion when testing cdddomains
     
    lines=open(infile, 'r').readlines()
    lines=(row.strip().split() for row in lines if len(row.strip().split())==14)

    ### _make method doesn't work for my class, so can't use below
#    for domCDD in map(DomainCDD._make, lines ):
#        print 'woot', domCDD
    
    ### I can create a dictionary for my data and instantiate my class through it ###
    ### BAD BECAUSE I NEED TO IMPORT STRICT_FIELDS; ABOVE METHOD IMPLICITLY WORKS ###
    return [DomainCDD(**dict(zip(strict_fields.keys(), line))) for line in lines] 

def to_dic(iterable, keyfield=None):
    ''' Take in an interable of DomainsCDD object, return a dictionary keyed automatically
    by record method, get_unique_key.  Keyfield can also accept a valid attribute of DomainCDD'''
    from cdd_domains import ManagerCDD
    if keyfield==None:
        return ManagerCDD((v.get_uniquekey(), v) for v in iterable)
    kget=attrgetter(keyfield)    
    return ManagerCDD((kget(v), v) for v in iterable)

### Methods in particluar to making custom domain analysis.  Not general, core methods. ###
from utils import sortbyarg


def formatted_domains(cd_dic):
    ''' Keys QueryAccessions to their domains ie: 'xp2343242.2 : cl002343, cl002343, cl202032.  This requires sorting to
        retain the domains in their positional order; therefore, an optional **kwargs parameter will accept a presorted 
        dictionary.  Otherwise, this module will make a sorted copy of the superfams dic to use.
        '''
    domains=sortbyarg(cd_dic, 'Accession', 'Start')  #Sorting is still suceptible to string sorting issues
    fdic={}
    for dom in domains:
        if dom.Accession not in fdic.keys():
            fdic[dom.Accession]=[]
        fdic[dom.Accession].append(dom.DomAccession)
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
    