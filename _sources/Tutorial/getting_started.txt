Getting Started
===============



CDD Class
---------

For now, the main data container is a class called the **DomainCDD** class.  For now, this is merely an immutable record class that is created from my `pyrecords project`_.  Essentially, it is a named tuple with extra functionality.   This means that it is immutable and as the project grows, I may opt to supplant this with a mutable object type.  The choice to choose an immutable record was mainly because these take up very little space in memory and are easy to work with.  
　
.. _pyrecords project: http://hugadams.github.com/pyrecords

Data Fields
-----------

The CDD class supports output from the CD-Batch search tool.  If a user uploads a set of protein sequences, the domains within the sequence are returned.  Here is some output from a real cdd file:

**Q#3** **-** **>SPU_018904**	**superfamily**	**208873**	**361**	**413**	**2.00744e-22**	**97.2737**	**cl08327**	**Glyco_hydro_47** **superfamily**	**C**	 **-**

This is actually 14 fields, although it may be difficult to see.  As such, the container class stores them in the following 14 attribute names.  


**Query** - Refers back to the protein to which the current domain belong.  Referencing by the numerical order proteins were input to the batch cd-search.  For example Q#10 means the current domain belongs to the tenth protein entered in the batch.

**u1** - N/A

**Accession** - GI Accession number `of the protein` to which this domain belongs.  (Note, '>' is stripped internally to be compatible with BioPython Sequence class). 

**Hittype** - Describes an NCBI CDD parameter which more or less corresponds to them manner by which the domain was characterized into the database.  Specific hits, for example, are hand-aligned; whereas, the designation of *superfamily* generally is a bit different.  Refer to the `NCBI CDD`_ for a better explanation.

.. _NCBI CDD: http://www.ncbi.nlm.nih.gov/Structure/cdd/cdd.shtml

**PSSMID** - Unique integer identifier for a cd-domain.

**Start** - Position along the peptide sequence at which the domain begins.

**End** - Position along the peptide sequence at which the domain ends.

**Eval** - Evalue score for domain identification.  Again, more information on how this is computed is available through `NCBI CDD`_. 

**Score** - Heuristic score of domain match.

**DomAccession** - Accession corresponding to the domain (not protein accession).  cl02432 is the domain accession for c-type lectin domain. 

**DomShortname** - Unique short name corresponding to the domain accession.  Eg Clect is the shortname to the c-type lectin domain.

**Matchtype** - Not sure how this is different from hit type at the moment.

**u2**  - N/A

**u3**  - N/A

**sequence** - *New* reserved slot to store the sequence corresponding to the region along the protein to which the domain identifies.  This is not implicitly returned by the NCBI CD Search tool for whatever reason.

Manual Instantion
-----------------

Let's see how it easy it is to instantiate a CD Domain object.  First, I'm going to demonstrate a manual instantiation; however, in practice, almost all input will be from batch files.  This input style is explained in the `pyrecords project`_ more thoroughly.  Records are generated first by inputing the immutable manager class, in this case, it is called *domain_manager*.

.. sourcecode:: ipython

   In [2]: from DataTypes.cdd_fields import domain_manager

Taking my example string:

**Q#3** **-** **>SPU_018904**	**superfamily**	**208873**	**361**	**413**	**2.00744e-22**	**97.2737**	**cl08327**	**Glyco_hydro_47** **superfamily**	**C**	 **-**

I will pass this as a list into my domain_manager.  This is very similar to namedtuple syntax, but pyrecords is automatically converting all of the attributes to their proper types.  For example, the attribute *Start* will be converted into an integer directly.

.. sourcecode:: ipython

   In [9]: fake_domain=fake_domain.strip().split()

   In [10]: domain=domain_manager._make(fake_domain, extend_defaults=True)
   In [11]: domain

   Out[11]: DomainCDD(Query='Q#3', u1='-', Accession='>SPU_018904', Hittype='superfamily', PSSMID=208873, Start=361, End=413, Eval=2.00744e-22, Score=97.2737, DomAccession='cl08327', DomShortname='Glyco_hydro_47', Matchtype='superfamily', u2='C', u3='-', sequence='')

Now I have complete attribute access with the correct field types.  

.. sourcecode:: ipython

   In [13]: domain.Accession, domain.Score
   Out[13]: ('>SPU_018904', 97.2737)

   In [15]: type(domain.Accession), type(domain.Score) 
   Out[15]: (str, float)


From File
---------

For now, only the batch output of NCBI's CD Search is supported.  The file reader function is merely a small wrapper around the pyrecords from_file() function.








　

　

　
