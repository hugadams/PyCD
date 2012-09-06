import sys
sys.path.append('/home/glue/Dropbox/pyrecords')

from Core.immutablemanager import ImmutableManager
#from Core.mutablemanager import MutableManager

#####################################################################################
## Defines basic fields and instantiates an immutable record type for storing data ##
#####################################################################################

### Define my fields, types and default values in one go, all of which are passed to the record manager
domain_fields=(('Query',str()), ('u1',str()), ('Accession',str()), ('Hittype',str()), ('PSSMID',int()), \
     ('Start',int()), ('End',int()), ('Eval',float()), ('Score',float()), ('DomAccession',str()), \
     ('DomShortname',str()), ('Matchtype',str()), ('u2',str()), ('u3',str()), ('sequence',str()) )

### Create immutable class called DomainCDD that has strict typechecking
domain_manager=ImmutableManager('DomainCDD', domain_fields)
