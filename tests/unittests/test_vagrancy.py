"""
Unit tests of the vagrancy.client module.

Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
All rights reserved.
This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl) and
is released under the "BSD 3-Clause License". Please see the LICENSE file that
is included as part of this package.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
from unittest import TestCase

from vagrancy import client


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class VagrancyTest(TestCase):
    """Test the :mod:`vagrancy.client` module."""

    def test_inventory(self):
        """vagrancy.client: Test the inventory method."""
        vagrancy_client = client.Vagrancy("http://no.vagrancy.here.net")
        with self.assertRaises(ConnectionRefusedError):
            vagrancy_client.inventory()


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
