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