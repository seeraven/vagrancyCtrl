# -*- coding: utf-8 -*-
"""
Module for accessing a vagrancy instance.

Vagrancy stores the boxes for different versions and different providers in the
following way:

  - Each box has a unique name consisting of ``<username>/<name>``.
  - Each box has one or more versions. The version can be anything like a
    semantic version number, e.g., ``1.2.3``, or strings like ``alpha``.
  - Each version of a box has one or more providers, e.g., ``virtualbox`` or
    ``libvirt``. Like for the version number, there are no constraints enforced
    by vagrancy.

Copyright:
    2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>

    All rights reserved.

    This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
    and is released under the "BSD 3-Clause License". Please see the ``LICENSE`` file
    that is included as part of this package.
"""
