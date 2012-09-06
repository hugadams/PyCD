##### Utilities functions for operating on individual DomainCDD objects and dictionaries of tem.
##### Not type checked and argument names are kept intentionally generic to 
##### encourage reuse.
from operator import attrgetter, itemgetter

###### Utilities to operate on a single DomainCDD instance 
### Note, all namedtuple methods are already inherited
### http://docs.python.org/library/collections.html#collections.namedtuple 

def from_file(manager, infile):
    ''' Take in CDD superfamilies file and creates namedtuples.  Requires RecordManager object passed 
    in as well. Note, parser only enforces that lines of
    the correct length are added.  Types are automatically set.'''
         
    lines=open(infile, 'r').readlines()
    lines=(row.strip().split() for row in lines if len(row.strip().split())==14)
    return tuple([manager._make(line, warning=False) for line in lines])

def get_uniquekey(obj):
    ''' Takes in DomainCDD tuple and returns a key based on a superposition of custom attributes'''
    return ("%s_%s_%s_%s"% (obj.Query, obj.PSSMID, obj.Start, obj.End))   

####### Utilities designed for dictionary of DomainCDD objects 
####### (not type checked; terminology purposly generic) 
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

def to_dic(iterable, keyfield=None):
    ''' Take in an interable of DomainsCDD object, return a dictionary keyed automatically
    by record method, get_unique_key.  Keyfield can also accept a valid attribute of DomainCDD'''
    if keyfield==None:
        return dict((get_uniquekey(v), v) for v in iterable)
    kget=attrgetter(keyfield)    
    return dict((kget(v), v) for v in iterable)

def histogram(cd_dic, *fields):
    ''' Returns count of unique occurrences for a field in CDDomain record.  Literally it is counting the
    occurrences of a unique attribute.  In practice, this is useful for understanding the domain distribution
    in the dataset.  Build to take in multple fields for flexibility.'''
    out={}
    for k, valuelist in get_fields(cd_dic, *fields).items():
        unique=list(set(valuelist))
        out[k]=tuple([(v, valuelist.count(v)) for v in unique])
    return out    

### Following methods are for data filtering.  Most likely already built into database functionality like SQL ###
def filter_if(dic, **keyvals):
    ''' Iterate through dictionary, return entries if all passed attribute are equal.  For multiple
    attributes, can pass special keyword, "criteria" which can have values 'all' or 'any'.  
    If 'all', then all fields must be identical to retain object.  If 'any', then only one field must be.'''
    out={}
    criteria=kwargs.pop('criteria', 'all')
    fget=attrgetter(**keyvals)
    pass   #FINISH

def filter_by(dic, **keyvals):
    ''' Pass numerical attributes in, will return all values that meet the 'criteria'.  The filter
    criteria keywords are "equal", "lessequal", "less", "greaterequal", "greater" '''
    validcrit=['equal', 'lessequal', 'less', 'greaterequal', 'greater']
    criteria=kwargs.pop('criteria', 'equal')
    if validcrit == 'equal':
        pass
    elif validcrit == 'lessequal':
        pass        
    elif validcrit == 'less':
        pass
    elif validcrit == 'greaterequal':
        pass
    elif validcrit == 'greater':
        pass    
    else:
        raise KeyError('Criteria messed up in filter_bny') #Replace later
    
def dic_to_file(dic, outfilename, delim='\t'):
    ''' Used to output a dictionary to a file whose values are iterables.  LATER MAKE IT BE ABLE TO TAKE IN 
    SINGLE VALUED VALUES SO IT WORKS FOR ITERABLES AND SINGLEVALUES.'''
    f=open(outfilename, 'w')
    for item in dic.items():
#        if type(value) == str:
 #           outstring=            
        outstring=key + delim + delim.join(value) + '\n'
        f.write(outstring)
    f.close() 