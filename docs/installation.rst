Installation
============

Requirements
------------

* Python 3.8 or higher
* Access to a CyPerf Controller (IP address and credentials)
* Network connectivity to the CyPerf Controller

Dependencies
------------

The following packages are required:

* ``cyperf`` – Official CyPerf SDK from Keysight
* ``pandas`` – For statistics visualization and DataFrame support
* ``sphinx`` – For documentation generation (development only)
* ``sphinx-rtd-theme`` – Read the Docs theme (development only)

Installation from Source
------------------------

Clone the repository and install in development mode:

.. code-block:: bash

   git clone https://github.com/your-username/cyperf_restpy.git
   cd cyperf_restpy
   pip install -r requirements.txt
   pip install -e .

Installation from PyPI
----------------------

*Coming soon*

.. code-block:: bash

   pip install cyperf-restpy

Verifying Installation
----------------------

After installation, verify that the package is correctly installed:

.. code-block:: python

   from cyperf_restpy.cyperf_scripts.cyperf_authorization import CyperfAuthorization
   print("Installation successful!")

SSL Certificate Warnings
------------------------

By default, CyPerf Controllers use self-signed SSL certificates. The library disables
SSL verification warnings automatically. If you prefer to suppress these warnings
explicitly in your scripts:

.. code-block:: python

   import urllib3
   urllib3.disable_warnings()

Development Installation
------------------------

For development with documentation and testing support:

.. code-block:: bash

   git clone https://github.com/your-username/cyperf_restpy.git
   cd cyperf_restpy
   pip install -r requirements.txt
   pip install -e .

   # Build documentation locally
   cd docs
   make html

   # Run tests
   cd ..
   python -m pytest tests/
