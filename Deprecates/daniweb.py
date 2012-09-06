from collections import namedtuple, OrderedDict
from record import recordtype

### Define my fields, types and default values in one go, all of which are passed to the Record class
### Types will be set permanently based on default value.
strict_fields=OrderedDict(
    (('Name',str('unnamed')), ('Age',int(18)),\
     ('Income',float(43000)), ('FamilyMembers',list()))
)


class Record(recordtype('Record', strict_fields.keys(), verbose=False, field_defaults=strict_fields)):
    ''' recordtype is a factory function returns a class very similar to namedtuple except that it is 
        mutable and also understands defaults values natively. Otherwise, it behaves the same way as a namedtuple-
        it is lightweight and very easy to subclass and interface to file input/output.  
        This class, Record, subclasses the mutable namedtuple and enforces typecasting and typchecking
        on all fields.  All types and defaults are automatically infered from the strict_fields global.'''

    def __init__(self, **kwargs):
        ''' Initializes all values based on __init__ inherited from MutableNamedTuple.  SetAttr will
        be called by default on each kwarg so I don't need to call _check from here.'''
        super(Record, self).__init__(**kwargs)
        print 'Creating %s'% self.__repr__()

    def __setattr__(self, attr, value):
        ''' Performs additional validation each time an attribute is set.'''
        value=self._check(attr, value)
        super(Record, self).__setattr__(attr, value)

    def _check(self, attr, value, warnings=True):
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
                    print attr, value, argtype, newvalue, fieldtype, 'here'
                    print ('Recasting Attr. %s = %s (%s) to %s (%s)')%(attr, value, argtype, newvalue, fieldtype)
                    return newvalue
        return value

    def get_key_value(self):
        ''' Return record as a key value pair for easy input into a **kwargs of a dictionary.
            Can customize this for many use cases.  For now, will just key by Name_age'''
        return ( ('%s_%s')%(self.Name, self.Age), self)

class ManagerError(ValueError):
    '''Custom error for failed typechecking in RecordManager class'''
    def __init__(self, entry):
        self.entry=entry
    def __str__(self): 
        return repr('RecordManager requires Record object input not \
                %s %s' % (self.entry, str(type(self.entry)))  )    

class RecordManager(dict):
    ''' Dictionary subclass used to manage records.  Keys can be automatically assigned or passed in manually.
        typecheck: Gives the user the option to be very pedantic and make sure all records are strictly of the
        Record type.  It's good to have the option; however, easy enough to turn off and be more Pythonic.'''

    def __init__(self, **kwargs): 
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
        self.update(**kwargs) 

    __getattr__ = dict.__getitem__  

        ### OVERWRITING THIS MESSES STUFF UP ###
    def __setattr__(self, attr, value):
        ''' Allow for attribute access of values with optional typechecking.  This is called anytime a user
            defines a new attribute, unless we are actually setting the typechecking attribute itself.'''
            
        if attr != 'typecheck':
            if self.typecheck:
                self._check_me(value)
        self.__dict__[attr] = value
   
    def __setitem__(self, key, value):
   #     self._typecheck(value)
        super(RecordManager, self).__setitem__(key, value)
       

    def update(self, **kwargs):
        ''' User can either pass a list of Records in (*args), then keys will automatically be
            generated from the name_and_age calculated field.  If a dictionary is passed (**kwargs) .  
            If typecheck is on, all entries will be screened.'''

        ### Kwargs lets user pass dictionary with custom keys    
        for key in kwargs:
          if self.typecheck:
              self._check_me(kwargs[key])
          self[key] = kwargs[key]

    def _check_me(self, value):
        '''Typecheck a value to ensure it is of the Record class.  Maybe pedantic; however, will be helpful
           to reduce errors for new users in the codebase who are unfamiliar with good input habits'''
        stricttype=Record  #Can make this a list if more than one type are acceptable
        if not isinstance(value, stricttype):  
            raise ManagerError(value)        

    def __str__(self):  
        ''' Custom printout, just for fun'''
        return '\n'.join('%s = %s Custom info here' % v for v in self.items())


if __name__ == '__main__':	
    #####------- Initiate Records -------######
    print '\n Making some records manually'
    record1=Record()  #Default attributes use
    record2=Record(Name='Adam') #Manually set one attribute, 
    record3=Record(Name='Bill', Age=30, Income=32000.0, FamilyMembers=['Regina', 'Betty'] )
    
    #####------- Set Values -------######
    print '\nWe can get or set access information through attribute or index lookup'
    print record2[0], record2.Name
    print '\nChanging name to Brutus'
    record2.Name='Brutus'
    print record2[0], record2.Name

    #####------- Take semi-bad input like a boss -------######
    print '\nSmart enough to handle some mistyped inputs...'
    record4=Record(Name=7000, Age=str(35), Income=32000, FamilyMembers=tuple(['Sandy', 'Jessy']))

    #####------- Populate the manager class (manual keys) -------######
    print '\nOk, lets put all these records into the RecordManager storage object'
    print '\nI will pass some through by assigning them keys "r1, r2, r3"'
    all_records=RecordManager(r1=record1, r2=record2, r3=record3, typecheck=False)

    #####------- Populate the manager class (automatic keys)-------######
    (k,v)=record1.get_key_value() #This works just sep out key and value
    print '\nAdding a record with an automatically generated key, %s \n'% k
    all_records[k]=v
    print k, v

    #####------- Demonstrate how turning off typechecking allows flexible input######
    print '\nBecause I set typecheck to False, the dictionary doesnt care what type the values are.'
    print'\nI will overwrite the value by attribute and then by index'
    all_records.r1='Just a string' #Prevents bad overwrite
    print all_records.r1, 'new value for r1'
  

    #####------- Demonstrate how turning on typechecking forces stringent input######
    print '\nBecause I set typecheck to True, the dictionary errors when I pass a non-Record object for a value.'
    print'nI will overwrite the value by attribute and then by index'
    all_records.r1='Just a string' 
    print all_records.r1, 'new value for r1'  
    
    
    #####------- Extra (comment out above section) ##########
    print '\nJust an example of such bad input that the Record object cannot be created'
    r5=Record(Age='string input')
  
 ## FOR NOW THIS IS A BUG 
#    all_records['r1']='Yet another string'
#    print all_records['r1'], 'new value for r1'
#    print all_records['r1'], all_records.r1  #THESE SHOULD NOT BE DIFFERENT
#
 #   print '\nRecords can be accessed by index or attribute'
  #  print all_records['Brutus_18'], 'Lookup by index'
   # print all_records.Brutus_18, 'Attribute lookup'

    # print '\nIndeed, attribute setting still works at the record level as well as the level of the record\n'
    #all_records.Brutus_18.Age=23
    #  print 'Brutus age', all_records.Brutus_18.Age

    #  print 'I can add more records and not specify keywords, so default ones are still generated'
    # all_records.add_record(record3)