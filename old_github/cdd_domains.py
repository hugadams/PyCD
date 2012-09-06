from collections import namedtuple, OrderedDict
from record import recordtype
from recordtype_2011 import recordtype as newrecordtype
from utils import sortbyarg, get_subset, from_file, to_dic, histogram
from cddutils import formatted_domains
import sys


### Define my fields, types and default values in one go, all of which are passed to the record
### factory function
strict_fields=OrderedDict(
    (('Query',str()), ('u1',str()), ('Accession',str()), ('Hittype',str()), ('PSSMID',int()), \
     ('Start',int()), ('End',int()), ('Eval',float()), ('Score',float()), ('DomAccession',str()), \
     ('DomShortname',str()), ('Matchtype',str()), ('u2',str()), ('u3',str())  
     ))

class DomainCDD(recordtype('DomainCDD', strict_fields.keys(), verbose=False, field_defaults=strict_fields)):
#class DomainCDD(newrecordtype('DomainCDD', strict_fields.keys(), default=strict_fields)):

    ''' recordtype is a factory function returns a class very similar to namedtuple except that it is 
        mutable and also understands defaults values natively. Otherwise, it behaves the same way as a namedtuple-
        it is lightweight and very easy to subclass and interface to file input/output.  
        This class, DomainCDD, subclasses the mutable namedtuple and enforces typecasting and typchecking
        on all fields.  All types and defaults are automatically infered from the strict_fields global.'''

    def __init__(self, **kwargs):
        ''' Initializes all values based on __init__ inherited from MutableNamedTuple.  SetAttr will
        be called by default on each kwarg so I don't need to call _check from here.'''
        super(DomainCDD, self).__init__(**kwargs)
    #     print 'Creating %s'% self.__repr__()

    def __setattr__(self, attr, value):
        ''' Performs additional validation each time an attribute is set.'''
        value=self._check(attr, value)
        super(DomainCDD, self).__setattr__(attr, value)

    def _check(self, attr, value, warnings=False):
        ''' This ensures all set attributes may be recast into their default types as defined in the strict_fields
        variable.  The program will attempt to recast types (for example will convert str(90) to int(90) if possible.
        If attempts to recast result in an error, program will raise Attribute error.

        "Warnings":  Option to print a notice each time a variable is successfuly recast.  

        In the future, this
        can get really in depth, for example prohibiting the python-legal str to list conversion 
        (eg str(['hi']) = "['hi']") and really specifying the behavior of certain advanced recasts.'''

        attrfield=strict_fields[attr]
        fieldtype, argtype=type(attrfield), type(value)
        if not isinstance(value, fieldtype): #If type mismatch
            try:
                newvalue=fieldtype(value)  #Try recast
            except (ValueError,TypeError):   #Recast failed
                raise TypeError("Argument: %s is %s and %s could not be recast to, %s" % (value, argtype, fieldtype, attr))
            else:          #Recast successful
                if warnings:
                    print ('Recasting Attr. %s = %s (%s) to %s (%s)')%(attr, value, argtype, newvalue, fieldtype)
                return newvalue
        return value  
    

    def get_fields(self):
        ''' Wrapper function to remind user of the fields'''
        return self.__slots__  

    def get_allvals(self):
        ''' Wrapper function to get all values stored in tuple'''
        return self.__getstate__()

    def get_uniquekey(self):
        ''' Returns a unique identifier that is the query name, domain and start,end points of the domain'''
        return ("%s_%s_%s_%s"% (self.Query, self.PSSMID, self.Start, self.End))


class ManagerError(ValueError):
    '''Custom error called when an entry into the ManagerCDD type does not have a value that is a
       DomainCDD class.  Note, by default TypeError accepts *args parameter '''
    def __init__(self, entry):
        self.entry=entry
    def __str__(self): 
        return repr('MangerCDD requires DomainsCDD object input not '+ str(type(self.entry)))

class ManagerCDD(dict):
    ''' Dictionary subclass used to manage records.  Keys can be automatically assigned or passed in manually.
        typecheck: Gives the user the option to be very pedantic and make sure all records are strictly of the
        Record type.  It's good to have the option; however, easy enough to turn off and be more Pythonic.'''

    def __init__(self, *args, **kwargs): 
        ''' *args and **kwargs allow for flexible creation as I will demonstrate at runtime.  
            There is a special keyword argument called "typecheck" which if True will stringently
            enforce all values in dictionary are of the Record class.
            Sigh, in Python3 I'd be able to give typecheck a default value (eg typecheck=True) and
            still have **kwargs, but this is not possible in my 2.7 version.  Therefore, I have to make
            it a parameter.'''
    #      dict.__init__(self, **kwargs) #LEAVE UNCOMMENTED
        typecheck=False #Default value, may be overridden if found in kwargs
        if 'typecheck' in kwargs.keys():
            assert type(kwargs['typecheck'])==bool  #Replace with better exception later
            typecheck=kwargs.pop('typecheck')  #Set and pop
        print 'here'
        self.typecheck=typecheck
        self.update(*args, **kwargs) 

    __getattr__ = dict.__getitem__  

    ### OVERLOADING BASIC PYTHON DICTIONARY METHODS ###
    def __setattr__(self, attr, value):
        ''' Allow for attribute access of values with optional typechecking.  This is called anytime a user
            defines a new attribute, unless we are actually setting the typechecking attribute itself.'''

        if attr != 'typecheck':
            if self.typecheck:
                self._check_me(value)
        self.__dict__[attr] = value

    def __setitem__(self, key, value):
    #     self._typecheck(value)
        super(ManagerCDD, self).__setitem__(key, value)


    #def update(self, *args, **kwargs):
    #    ''' User can either pass a list of Records in (*args), then keys will automatically be
    #        generated from the name_and_age calculated field.  If a dictionary is passed (**kwargs) .  
    #        If typecheck is on, all entries will be screened.'''

    #    ### Kwargs lets user pass dictionary with custom keys    
   #     for key in kwargs:
  #          if self.typecheck:
 #               self._check_me(kwargs[key])
#            self[key] = kwargs[key]

    def __str__(self):  
        ''' Custom printout, just for fun'''
        return '\n'.join('%s = %s Custom info here' % v for v in self.items())

    ### METHODS RELATED TO VALIDATION ###
    def _check_me(self, value):
        '''Typecheck a value to ensure it is of the Record class.  Maybe pedantic; however, will be helpful
           to reduce errors for new users in the codebase who are unfamiliar with good input habits'''
        stricttype=Record  #Can make this a list if more than one type are acceptable
        if not isinstance(value, stricttype):  
            raise ManagerError(value)        





if __name__ == '__main__':	
    d0=DomainCDD()
    d1=DomainCDD(Query='steve', Start=20.0)
    d2=DomainCDD(Query='bo', Start=8.0)
    d3=DomainCDD(Query='gay', Start=50.0)
    print dir(d1), d1
    ds=(d1,d2,d3)
    dic=ManagerCDD()
    for d in ds:
        dic[d.get_uniquekey()]=d
#    print dic

  #  print sortbyarg(dic, 'Query', 'Start')
#    print get_subset(dic, 'Query', 'Start', newkey='Start')
    domains=from_file('cl02432_superfams.txt')
    print len(domains)
    dfile=to_dic(domains)
    fd=formatted_domains(dfile)
    h=histogram(dfile, 'DomAccession', 'Accession')
    print h
##################
######SCRAP#######
##################


class DomainCDD_Fresh(object):  #Alternative to named tuple basically that allows for mutability
    ''' Type checked record type for storing individual CDD records from NCBI database.'''
    __slots__ = 'height', 'width', 'length'
    def __init__(self, **kwargs):

        ### IT'S BETTER TO CHECK ALL TYPES.  IF THEY ARE NOT CORRECT, AT LEAST RAISE AN ERROR BEFORE AUTOCONVERTING.
        ### IF AUTOCONVERTING FAILS, VALUEERROR WILL BE RAISED.  

        ## SO FOR EXAMPLE, IF USER ENTERS 10 AND CODE CONVERTS TO 10.0, RAISES A WARNING; HOWEVER IF USER
        ## ENTIER 'SALLY' THEN CODE WILL BE PISSED AND AUTOMATICALLY RAISE ERROR

    #     fixedtypes=(int,int,int) #fixed regular format of type input
    #    for argno, argtype in enumerate(fixedtypes):
        #       if not isinstance(value

        self.height, self.width, self.length = int(height), width, length

    def get_uniquekey(self):
        ''' Returns a unique identifier that is the query name, domain and start,end points of the domain'''
        return str(self.height) + '_lol_' + str(self.width)

    def __str__(self):
        return 'DomainCDD(%s)' % ','.join('%s = %s' % (v, getattr(self, v)) for v in self.__slots__)