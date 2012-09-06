### Adam Hughes 8/7/12
### Record class which returns named tuples with same fields, similar syntax
### and the added options of defaults and a typechecking
from collections import namedtuple

class RecordManager(object):

    def __init__(self, typename, strict_fields, verbose=False):
        ''' Store all of the field and type data as class methods so they aren't regenerated
            everytime a new named tuple is required'''
        self.typename=typename 
    
        ### Store field type and default information in varous formats for easy access by methods ###
        self.strict_fields=strict_fields
        self._strict_names=[v[0] for v in strict_fields]
        self._strict_types=[ type(v[1]) for v in strict_fields ]
        self.strict_defaults=[ v[1] for v in strict_fields]  
        
        vars(self)[typename]=namedtuple(typename, self._strict_names, verbose=verbose)  #Creates a namedtuple class from factory function

    def _typecheck(self, arg, fieldtype, warning=False):
        ''' Takes in an argument and a field type and trys to recast if necessary, then returns recast argument'''
        if not isinstance(arg, fieldtype):   
            try:
                oldarg=arg            #Keep for error printout
                arg=fieldtype(arg)    #Attempt recast
            except (ValueError, TypeError):  #Recast failed
                raise TypeError("Argument: %s to %s" % (arg, fieldtype))
            else:
                if warning:
                    print ("Recasting %s to %s as %s" % (oldarg, fieldtype, arg) )        
        return arg
        
    def _make(self, args, **kwargs):        
        '''Typechecks arguments and populates with defaults for non-entered fields.  Returns namedtuple. 
           The special keyword "warning" will make the _typecheck method alert the user of recasting.
           warning: If true and if recast is true, prints warning each time an input field is successfully type recasted.
   
           Another keyword "extend_defaults" can be used if the user wants to enter data of only a few fields.  For example,
           if the user passes in field 0, this will autofill field 1, field 2 etc.. with defaults.  This may not be a useful
           method since the dict_make method implements this robustly via keywords.  '''                
        warning=kwargs.pop('warning', False)
        extend_defaults=kwargs.pop('extend_defaults', False)
        
        if len(args) > len(self.strict_defaults):
            raise ValueError('Too many arguments')
        
        ### If not enough args entered, fill in with strict defaults ###
        elif len(args) < len(self.strict_defaults) and extend_defaults==True: 
            args=list(args) 
            args.extend(self.strict_defaults[len(args):len(self.strict_defaults)] )       
            
        ### Typecheck arguments ###
        for i in range(len(args)):
                arg=args[i] ; fieldtype=self._strict_types[i]
                arg=self._typecheck(arg, fieldtype, warning)  #Will overwrite arguments as it goes
        return vars(self)[self.typename](*args)


    def dict_make(self, **kwargs):
        ''' User can pass a dictionary of attributes in and they will be typechecked/recast.  Similiar to passing
        dictionary directly to namedtuple using **d notation'''
        warning=kwargs.pop('warning', False)        

        for name, default in self.strict_fields:
            try:
                value=kwargs[name]
                print name, default
            except KeyError:
                kwargs[name]=default #Throw the default value in if missing
            else:
                value=self._typecheck(value, type(default), warning) #Typecheck if found
                kwargs[name]=value 
                
        return vars(self)[self.typename](**kwargs)
        

if __name__ == '__main__':	
    personfields=[
               ('name',str('unnamed') ), ('age',int() ), ('income',float() )
               ]
    ### Construct the class builder ###
    personmanager=RecordManager('Person', personfields)

    ### Get some people ###
    print '\nLets make some people\n'
    bill=personmanager._make(['Billy Gundam', 80, 10000.00])
    jill=personmanager._make(['Jill Blanks', 35, 15000.00])
    glue=personmanager._make(['glue', 32], extend_defaults=True)
    print bill
    print jill
    print glue

    
    print '\nThese are all still of type namedtuple, so all the builtin methods work\n'
    print '\nConversion to dictionary with _asdict()\n'
    print glue._asdict()
    print '\nNew named tuple with Field Replacement\n'
    print glue._replace(name='Not sara')
    
    ### TO MAKE: Let class take in keyword args to make objects from dict (mimicing **d), maybe
    ### may have to settle doing this from a new method like personmanager.fromdict()
    
    print '\nI can still subclass the namedtuple; although, now it defaults back to a namedtuple.  Extra \\\
    methods for subclassing need to be incoprorated.  Something like personmanager.subclass.\n'
    SuperPerson=namedtuple('SuperPerson', personmanager.Person._fields+ ('height', 'weight') )
    sara=SuperPerson('Sara Jenkins', 32.3, 32000, '6feet', '150lbs')
    print sara
    
    print '\nI can still refer directly to the class itself, which is sometimes necessary.  For example, \
           if I want to directly instantiate from a dictionary with **d notation.  Although, now defaults \
           and fields are nolonger enforced.\n'
    mydict={'name':'Jason', 'age': 30, 'income':4.0}
    jason=personmanager.Person(**mydict)
    print jason
    
    print '\nIf I want to pass a dictionary AND have it typechecked, there is a new method for that called \
          dict_make.  Note that the dictionary was incomplete and the default record value was returned instead\
          of returning an error!'
    freddict={'name':'Fred', 'age':32}
    fred=personmanager.dict_make(**freddict)
    print fred

    print '\nIf I tried to instantiate a named tuple directly with an incomplete dictionary, I would get an error'
    try:
        fred=personmanager.Person(**freddict)
    except TypeError:
        print 'Yup I just errored big time'