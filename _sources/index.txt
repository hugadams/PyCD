.. PyCD documentation master file, created by
   sphinx-quickstart on Fri Aug 31 17:29:15 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyCD
===============

PyCD is preliminary Python framework for performing protein domain analysis, particularly NCBI's `Conserved Domain Database`_.  This project stemmed from research at the George Washington University, the goal of which was to characterize lectin-binding domains in the purple sea urchin.  As such, it aims to provide both *scripts* and an *API* for conserved domain (CD) analysis.

What's New:
----------

I finally created this site which is generously hosted by GitHub_.  The `source code`_ is available for download; however, the API is not in a tractable state.  I will address this soon so that others can easily use this package.  

.. _source code: https://github.com/hugadams/PyCD

.. _GitHub: https://github.com


On the Horizon
--------------

* More integration with BioPython, especially sequence-based methods and Blast functionality.
* An API and setup.py installation file for PyCD and PyRecords.
* Full scripts for canned analysis routines.
* TraitsUI interface for domain comparisons.

Check back soon for updates.

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   Tutorial/installation_dependencies.rst
   Tutorial/getting_started.rst
   API/pycd.rst


.. _Conserved Domain Database: http://www.ncbi.nlm.nih.gov/Structure/cdd/cdd.shtml


Index and Search
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

