# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Unit tests of the vagrancy.box module."""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import json
import os
from unittest import TestCase

import requests_mock

import vagrancy.box


# -----------------------------------------------------------------------------
# Test Infos
# -----------------------------------------------------------------------------
def init_box_map(name):
    """Initialize a box map suitable for a convertion to JSON."""
    return {"name": name, "versions": []}


def init_version(box_map, version):
    """Add a new version information to a box map."""
    box_map["versions"].append({"version": version, "providers": []})


def add_provider(box_map, version, provider, base_url = "http://mock.vagrancy.net"):
    """Add a new provider information to a version of a box map."""
    for version_entry in box_map["versions"]:
        if version_entry["version"] == version:
            version_entry["providers"].append({"name": provider,
                                               "url": os.path.join(base_url,
                                                                   box_map["name"],
                                                                   version,
                                                                   provider)})


TEST_BOX_MAP = init_box_map("user/test")
init_version(TEST_BOX_MAP, "1.2.3")
add_provider(TEST_BOX_MAP, "1.2.3", "virtualbox")
add_provider(TEST_BOX_MAP, "1.2.3", "libvirt")
init_version(TEST_BOX_MAP, "1.2.4")
add_provider(TEST_BOX_MAP, "1.2.4", "virtualbox")
init_version(TEST_BOX_MAP, "bionic")
add_provider(TEST_BOX_MAP, "bionic", "vmware")


# -----------------------------------------------------------------------------
# Test Class
# -----------------------------------------------------------------------------
class VagrancyBoxTest(TestCase):
    """Test the :class:`vagrancy.box.Box` class."""

    @requests_mock.mock()
    def test_valid_constructor(self, mock_get):
        """Box.__init__(): Valid arguments."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test")
        # pylint: disable=W0212
        self.assertEqual(box._server_url, "http://mock.vagrancy.net")
        self.assertEqual(box.box_name, "user/test")
        self.assertFalse(box.is_empty())

        self.assertIn("1.2.3", box.version_provider_map)
        self.assertIn("virtualbox", box.version_provider_map["1.2.3"])
        self.assertIn("libvirt", box.version_provider_map["1.2.3"])
        self.assertIn("1.2.4", box.version_provider_map)
        self.assertIn("virtualbox", box.version_provider_map["1.2.4"])
        self.assertNotIn("libvirt", box.version_provider_map["1.2.4"])
        self.assertIn("bionic", box.version_provider_map)
        self.assertIn("vmware", box.version_provider_map["bionic"])

        self.assertIn("virtualbox", box.provider_version_map)
        self.assertIn("1.2.3", box.provider_version_map["virtualbox"])
        self.assertIn("1.2.4", box.provider_version_map["virtualbox"])
        self.assertIn("libvirt", box.provider_version_map)
        self.assertIn("1.2.3", box.provider_version_map["libvirt"])
        self.assertNotIn("1.2.4", box.provider_version_map["libvirt"])
        self.assertIn("vmware", box.provider_version_map)
        self.assertIn("bionic", box.provider_version_map["vmware"])

        self.assertEqual("1.2.4", box.provider_latest_versions["virtualbox"])
        self.assertEqual("1.2.3", box.provider_latest_versions["libvirt"])
        self.assertEqual("bionic", box.provider_latest_versions["vmware"])

        self.assertEqual("1.2.5", box.provider_next_versions["virtualbox"])
        self.assertEqual("1.2.4", box.provider_next_versions["libvirt"])
        self.assertEqual(None,    box.provider_next_versions["vmware"])

    @requests_mock.mock()
    def test_constructor_provider_pattern(self, mock_get):
        """Box.__init__(): Provider pattern."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test", "v*box")
        # pylint: disable=W0212
        self.assertEqual(box._server_url, "http://mock.vagrancy.net")
        self.assertEqual(box.box_name, "user/test")
        self.assertFalse(box.is_empty())

        self.assertIn("1.2.3", box.version_provider_map)
        self.assertIn("virtualbox", box.version_provider_map["1.2.3"])
        self.assertNotIn("libvirt", box.version_provider_map["1.2.3"])
        self.assertIn("1.2.4", box.version_provider_map)
        self.assertIn("virtualbox", box.version_provider_map["1.2.4"])
        self.assertNotIn("libvirt", box.version_provider_map["1.2.4"])

        self.assertIn("virtualbox", box.provider_version_map)
        self.assertIn("1.2.3", box.provider_version_map["virtualbox"])
        self.assertIn("1.2.4", box.provider_version_map["virtualbox"])
        self.assertNotIn("libvirt", box.provider_version_map)

        self.assertEqual("1.2.4", box.provider_latest_versions["virtualbox"])
        self.assertNotIn("libvirt", box.provider_latest_versions)

        self.assertEqual("1.2.5", box.provider_next_versions["virtualbox"])
        self.assertNotIn("libvirt", box.provider_next_versions)

    @requests_mock.mock()
    def test_constructor_empty_box(self, mock_get):
        """Box.__init__(): Provider pattern resulting in empty box."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test", "unknown")
        # pylint: disable=W0212
        self.assertEqual(box._server_url, "http://mock.vagrancy.net")
        self.assertEqual(box.box_name, "user/test")
        self.assertTrue(box.is_empty())

        self.assertTrue(len(box.version_provider_map) == 0)
        self.assertTrue(len(box.provider_version_map) == 0)
        self.assertTrue(len(box.provider_latest_versions) == 0)
        self.assertTrue(len(box.provider_next_versions) == 0)

    def test_invalid_constructor(self):
        """Box.__init__(): Invalid box name."""
        with self.assertRaises(ValueError):
            _ = vagrancy.box.Box("http://mock.vagrancy.net", "test")
        with self.assertRaises(ValueError):
            _ = vagrancy.box.Box("http://mock.vagrancy.net", "user/test/2")

    @requests_mock.mock()
    def test_get_filtered_box_files_default(self, mock_get):
        """Box.get_filtered_box_files(): Default arguments."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test")
        box_list = box.get_filtered_box_files()
        self.assertIn(box.provider_version_map["virtualbox"]["1.2.3"], box_list)
        self.assertIn(box.provider_version_map["virtualbox"]["1.2.4"], box_list)
        self.assertIn(box.provider_version_map["libvirt"]["1.2.3"], box_list)

    @requests_mock.mock()
    def test_get_filtered_box_files_version_pattern(self, mock_get):
        """Box.get_filtered_box_files(): Version pattern."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test")
        box_list = box.get_filtered_box_files(version_pattern = "1.?.4")
        self.assertNotIn(box.provider_version_map["virtualbox"]["1.2.3"], box_list)
        self.assertIn(box.provider_version_map["virtualbox"]["1.2.4"], box_list)
        self.assertNotIn(box.provider_version_map["libvirt"]["1.2.3"], box_list)

    @requests_mock.mock()
    def test_get_filtered_box_files_provider_pattern(self, mock_get):
        """Box.get_filtered_box_files(): Provider pattern."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test")
        box_list = box.get_filtered_box_files(provider_pattern = "v*box")
        self.assertIn(box.provider_version_map["virtualbox"]["1.2.3"], box_list)
        self.assertIn(box.provider_version_map["virtualbox"]["1.2.4"], box_list)
        self.assertNotIn(box.provider_version_map["libvirt"]["1.2.3"], box_list)

    @requests_mock.mock()
    def test_get_filtered_box_files_latest_version(self, mock_get):
        """Box.get_filtered_box_files(): Latest version."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test")
        box_list = box.get_filtered_box_files(version_pattern = "+1")
        self.assertNotIn(box.provider_version_map["virtualbox"]["1.2.3"], box_list)
        self.assertIn(box.provider_version_map["virtualbox"]["1.2.4"], box_list)
        self.assertIn(box.provider_version_map["libvirt"]["1.2.3"], box_list)

    @requests_mock.mock()
    def test_get_filtered_box_files_oldest_versions(self, mock_get):
        """Box.get_filtered_box_files(): Oldest versions."""
        mock_get.get("http://mock.vagrancy.net/user/test",
                     text=json.dumps(TEST_BOX_MAP))

        box = vagrancy.box.Box("http://mock.vagrancy.net", "user/test")
        box_list = box.get_filtered_box_files(version_pattern = "-1")
        self.assertIn(box.provider_version_map["virtualbox"]["1.2.3"], box_list)
        self.assertNotIn(box.provider_version_map["virtualbox"]["1.2.4"], box_list)
        self.assertNotIn(box.provider_version_map["libvirt"]["1.2.3"], box_list)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
