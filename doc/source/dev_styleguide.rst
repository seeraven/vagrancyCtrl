Style Guide
===========

Header
------

The header of the python source files should look like

.. code-block:: python

   # -*- coding: utf-8 -*-
   #
   # Copyright (c) 2020, Clemens Rabe <clemens.rabe@clemensrabe.de>
   # All rights reserved.
   #
   # Redistribution and use in source and binary forms, with or without
   # modification, are permitted provided that the following conditions
   # are met:
   #
   # 1. Redistributions of source code must retain the above copyright
   #    notice, this list of conditions and the following disclaimer.
   #
   # 2. Redistributions in binary form must reproduce the above copyright
   #    notice, this list of conditions and the following disclaimer in the
   #    documentation and/or other materials provided with the distribution.
   #
   # 3. Neither the name of Clemens Rabe, nor the names of its contributors
   #    may be used to endorse or promote products derived from this software
   #    without specific prior written permission.
   #
   # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   # "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   # LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   # A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   # HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   # SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
   # TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
   # PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
   # LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
   # NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   # SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
   #
   '''
   This python module ...
   '''

Repeating the license in every file might seem some overkill, but it has the
advantage of having it already in place when extracting individual parts of
into other applications or projects.


Style Guide for Python Code
---------------------------

The python source files must be formatted according to the python PEP8_ style
that is also checked by the pycodestyle_ and pylint_ tools. To perform the
checks, call:

.. code-block:: bash

   make pycodestyle
   make pylint

The only exception to the PEP8_ style is a not so strict interpretation of
whitespaces. This is configured in the configuration files :code:`config/pylintrc`
and :code:`config/pycodestyle`. The reason is to allow a more readable formatting
as shown in the following example:

.. code-block:: python

   # Our style:
   RESET   = "\033[0m"
   COLOR   = "\033[1;%dm"
   BOLD    = "\033[1m"
   BLACK   = COLOR % 30
   RED     = COLOR % 31
   GREEN   = COLOR % 32
   YELLOW  = COLOR % 33
   BLUE    = COLOR % 34
   MAGENTA = COLOR % 35
   CYAN    = COLOR % 36
   WHITE   = COLOR % 37
		
   parser.add_argument('--no-defaults',
                       dest    = 'use_defaults',
                       action  = 'store_false',
                       default = True,
                       help    = 'When no matches are generated, '
                       'do not fallback to readline\'s default completion')

   # Strict PEP8:
   RESET="\033[0m"
   COLOR="\033[1;%dm"
   BOLD="\033[1m"
   BLACK=COLOR % 30
   RED=COLOR % 31
   GREEN=COLOR % 32
   YELLOW=COLOR % 33
   BLUE=COLOR % 34
   MAGENTA=COLOR % 35
   CYAN=COLOR % 36
   WHITE=COLOR % 37
		
   parser.add_argument('--no-defaults',
                       dest='use_defaults',
                       action='store_false',
                       default=True,
                       help='When no matches are generated, '
                       'do not fallback to readline\'s default completion')


Style Guide for Inline Documentation
------------------------------------

For the documentation, all elements must be documented for sphinx_ using the
`Google Python Style Guide`_. See also the `Google Python Style Guide Example`_.


.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _pycodestyle: https://pypi.org/project/pycodestyle/
.. _pylint: https://www.pylint.org/
.. _sphinx: http://www.sphinx-doc.org/en/master/
.. _`Google Python Style Guide`: https://github.com/google/styleguide/blob/gh-pages/pyguide.md
.. _`Google Python Style Guide Example`: http://www.sphinx-doc.org/en/master/usage/extensions/example_google.html
