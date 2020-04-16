Development Documentation
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   dev_styleguide
   dev_workflow
   dev_manage_3rdParty_modules
   dev_unittests
   API Documentation <apidoc/vagrancy>


Development Support
-------------------

To ensure a high quality software product, the following topics are covered
through various tools:

- A common style guide:

  - Ensuring a common style, here the PEP8 style, by using the tool pycodestyle_.
    The style can be checked by calling :code:`make pycodestyle`.

- A well tested software:
    
  - Performing a static code analysis using the tool pylint_. To perform the
    static code analysis, call :code:`make pylint`.
  - Ensure the functionality of the individual components by performing unit-tests
    using nose_. To execute the tests, call :code:`make unittests`.  
  - Ensure the functionality of the application by performing various custom
    `blackbox` tests. To execute the tests, call :code:`make tests`.
  
- A documentation:
    
  - Generate the user and developer documentation using sphinx_. To generate the
    documentation, call :code:`make doc`.
  - Changes are documented in the `git` repository. By enforcing a common style
    on the commit messages through git hooks, these comments can directly be
    used to generate a `Changelog`.
  
- A development workflow:
    
  - The development workflow as described below can not be enforced, but is
    highly encouraged.


However, the following topics are not automatically checked and need therefore
special attention:

- Checking documentation coverage.
- Checking blackbox test coverage.


.. _pycodestyle: https://pypi.org/project/pycodestyle/
.. _pylint: https://www.pylint.org/
.. _sphinx: http://www.sphinx-doc.org/en/master/
.. _nose: https://nose.readthedocs.io/en/latest/
