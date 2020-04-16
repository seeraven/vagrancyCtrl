# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Unit tests of the vagrancy.client module."""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
from unittest import TestCase, mock

import requests

from vagrancy import client


# -----------------------------------------------------------------------------
# Mock of requests.get
# -----------------------------------------------------------------------------
def mocked_requests_get(*args, **_):
    """Mock function for requests.get()."""
    # pylint: disable=R0903
    class MockResponse:
        """Mock response of a requests.get() call."""

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """Return the JSON data."""
            return self.json_data

    if args[0] == 'http://mock.vagrancy.net/inventory':
        return MockResponse({"boxes": []}, 200)

    return MockResponse(None, 404)


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class VagrancyClientInventoryTest(TestCase):
    """Test the :meth:`vagrancy.client.Vagrancy.inventory` method."""

    def test_inventory_connection_error(self):
        """Vagrancy.inventory(): Test with an invalid URL."""
        vagrancy_client = client.Vagrancy("http://no.vagrancy.here.net")
        with self.assertRaises(requests.exceptions.ConnectionError):
            vagrancy_client.inventory()

    @mock.patch('vagrancy.client.requests.get', side_effect=mocked_requests_get)
    def test_inventory_old_vagrancy(self, mock_get):
        """Vagrancy.inventory(): Test with an old vagrancy server."""
        vagrancy_client = client.Vagrancy("http://mock.oldvagrancy.net")
        with self.assertRaises(ConnectionRefusedError):
            vagrancy_client.inventory()
        self.assertEqual(len(mock_get.call_args_list), 1)

    @mock.patch('vagrancy.client.requests.get', side_effect=mocked_requests_get)
    def test_inventory_empty(self, mock_get):
        """Vagrancy.inventory(): Test with an empty response."""
        vagrancy_client = client.Vagrancy("http://mock.vagrancy.net")
        boxes = vagrancy_client.inventory()
        self.assertEqual(len(boxes), 0)
        self.assertEqual(len(mock_get.call_args_list), 1)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
