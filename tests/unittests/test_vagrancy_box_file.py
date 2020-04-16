# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Unit tests of the vagrancy.box_file module."""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import os
from unittest import TestCase

import requests_mock

from testfixtures import TempDirectory

import vagrancy.box_file


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class VagrancyBoxFileTest(TestCase):
    """Test the :class:`vagrancy.box_file.BoxFile` class."""

    def test_valid_constructor(self):
        """BoxFile.__init__(): Valid arguments."""
        box = vagrancy.box_file.BoxFile("http://mock.vagrancy.net",
                                        "user/test", "1.0.0", "virtualbox")
        self.assertEqual(box.box_name, "user/test")
        self.assertEqual(box.version, "1.0.0")
        self.assertEqual(box.provider, "virtualbox")

    def test_invalid_constructor(self):
        """BoxFile.__init__(): Invalid box name."""
        with self.assertRaises(ValueError):
            _ = vagrancy.box_file.BoxFile("http://mock.vagrancy.net",
                                          "test", "1.0.0", "virtualbox")
        with self.assertRaises(ValueError):
            _ = vagrancy.box_file.BoxFile("http://mock.vagrancy.net",
                                          "user/test/2", "1.0.0", "virtualbox")

    def test_get_url(self):
        """BoxFile.get_url(): Correct box URL."""
        box = vagrancy.box_file.BoxFile("http://mock.vagrancy.net",
                                        "user/test", "1.0.0", "virtualbox")
        self.assertEqual(box.get_url(),
                         "http://mock.vagrancy.net/user/test/1.0.0/virtualbox")

    @requests_mock.mock()
    def test_delete(self, mock_delete):
        """BoxFile.delete(): Existing and non-existing boxes."""
        mock_delete.delete("http://mock.vagrancy.net/user/test/1.0.0/virtualbox")
        box = vagrancy.box_file.BoxFile("http://mock.vagrancy.net",
                                        "user/test", "1.0.0", "virtualbox")
        self.assertTrue(box.delete())

        mock_delete.delete("http://other.vagrancy.net/user/test/1.0.0/virtualbox",
                           status_code=404)
        box = vagrancy.box_file.BoxFile("http://other.vagrancy.net",
                                        "user/test", "1.0.0", "virtualbox")
        self.assertFalse(box.delete())

    @requests_mock.mock()
    def test_upload(self, mock_put):
        """BoxFile.upload(): Upload a box."""
        mock_put.put("http://mock.vagrancy.net/user/test/1.0.0/virtualbox",
                     status_code=201)
        with TempDirectory() as d:
            d.write('box', b'Dummy box')
            box = vagrancy.box_file.BoxFile("http://mock.vagrancy.net",
                                            "user/test", "1.0.0", "virtualbox")
            self.assertTrue(box.upload(os.path.join(d.path, 'box')))

    @requests_mock.mock()
    def test_download(self, mock_get):
        """BoxFile.download(): Downloat a box."""
        mock_get.get("http://mock.vagrancy.net/user/test/1.0.0/virtualbox",
                     text='Dummy Box')
        with TempDirectory() as d:
            box = vagrancy.box_file.BoxFile("http://mock.vagrancy.net",
                                            "user/test", "1.0.0", "virtualbox")
            self.assertTrue(box.download(os.path.join(d.path, 'box')))


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
