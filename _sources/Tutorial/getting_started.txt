Getting Started
===============



Introduction to containers and records:
--------------------------------------

　

Good programs always start by managing data in a flexible and robust manner. Python has great builtin container datatypes (lists, tuples, dictionaries), but often, we need to go beyond these and create flexible data handlers which are custom-fitted to our analysis. To this end, the programmer really does become an architect, and a myriad of possible approaches are applicable. This is a double-edged sword, though, as inexperienced coders (like me) will tend to go down the wrong avenues, and implement poor solutions. Emerging from such a trajectory, PyRecords is an attempt to ease the suffering.

　

Immutable containers:
--------------------

As far as immutable containers go, Python already has a nice builtin type for managing records- the underused `namedtuple <http://docs.python.org/library/collections.html#collections.namedtuple>`_. A namedtuple is an immutable array container just like a normal tuple, except namedtuples have field designations. Therefore, elements can be accessed by attribute lookup and itemlookup (ie x.a or x[0]); whereas, tuples have no concept of attribute lookup. Namedtuples are a really great option for storing custom datatypes for these reasons:

* They are lightweight (take up very little memory).

* They are easily interfaced to file or sql database I/O, but also can be declared in-code.

* They have many basic builtin utilities for quick container transformations (nametuple to dict for example).

　

　

　
