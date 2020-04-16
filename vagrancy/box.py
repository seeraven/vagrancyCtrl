# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""
Representation of a vagrant box stored on a vagrancy server.

This module specifies the class :class:`Box` that represents a box
identified by a name that has one or more versions with one or more
providers.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import fnmatch

import requests

from .box_file import BoxFile


# -----------------------------------------------------------------------------
# Class Definitions
# -----------------------------------------------------------------------------
class Box:
    """Representation of a vagrant box.

    This class represents a specific box identified by a name, with a specific
    version and a specific provider.

    Attributes:
        _server_url (str):          The vagrancy server base URL.
        box_name (str):             The box name confirming to ``<username>/<name>``.
        version_provider_map (map): A map with BoxFile entries. The indexing scheme
                                    is version_provider_map[version][provider].
        provider_version_map (map): A map with BoxFile entries. The indexing scheme
                                    provider_version_map[provider][version].
    """

    def __init__(self, server_url, box_name, provider_pattern = "*"):
        """Create a new Box object.

        Args:
            server_url (str):        The base URL of the vagrancy server.
            box_name (str):          The box name confirming to ``<username>/<name>``.
            provider_pattern (str):  A pattern to select matching providers.

        Raises:
            ValueError: If the `box_name` does not confirm to ``<username>/<name>``.
        """
        self._server_url = server_url
        self.box_name = box_name
        self.version_provider_map = {}
        self.provider_version_map = {}

        self.provider_latest_versions = {}
        self.provider_next_versions   = {}

        if self.box_name.count('/') != 1:
            raise ValueError("The argument box_name must contain exactly one '/'!")

        self.retrieve_box_data(provider_pattern)

    def retrieve_box_data(self, provider_pattern = "*"):
        """Retrieve the versions and providers of the box from the server."""
        response = requests.get("%s/%s" % (self._server_url, self.box_name))
        response_data = response.json()

        self.version_provider_map = {}
        self.provider_version_map = {}

        for version_entry in response_data['versions']:
            version = version_entry['version']

            for provider_entry in version_entry['providers']:
                provider = provider_entry['name']

                if fnmatch.fnmatch(provider, provider_pattern):
                    box_file = BoxFile(self._server_url, self.box_name, version, provider)

                    self.version_provider_map.setdefault(version, {}).setdefault(provider, box_file)
                    self.provider_version_map.setdefault(provider, {}).setdefault(version, box_file)

        self.provider_latest_versions = {}
        self.provider_next_versions   = {}

        for provider in self.provider_version_map:
            all_versions = list(self.provider_version_map[provider].keys())

            # Sort all versions assuming they are integers separated by dots.
            # If that does not work, use a lexical sort.
            try:
                all_versions.sort(reverse = True, key=lambda s: list(map(int, s.split('.'))))

                split_version                         = all_versions[0].split('.')
                split_version[-1]                     = str(int(split_version[-1]) + 1)
                self.provider_next_versions[provider] = '.'.join(split_version)

            # pylint: disable=W0702
            except:
                all_versions.sort(reverse = True)
                self.provider_next_versions[provider] = None

            self.provider_latest_versions[provider] = all_versions[0]

    def get_filtered_box_files(self, version_pattern = "*", provider_pattern = "*"):
        """Get a list of filtered BoxFile objects.

        Args:
            version_pattern (str): A pattern of the versions to select. The special string
            '-1' selects all except the latest version, the special string '+1' selects the
            only the latest version.
            provider_pattern (str): A pattern of the providers to select.

        Returns:
            list: A list of matching BoxFile objects.

        Raises:
            ValueError: If the version is not a semantic version number but contains
            other string literals.
        """
        box_list = []
        matching_providers = fnmatch.filter(self.provider_version_map.keys(), provider_pattern)

        for provider in matching_providers:
            all_versions = list(self.provider_version_map[provider].keys())

            if version_pattern == '-1':
                matching_versions = [i for i in all_versions
                                     if i != self.provider_latest_versions[provider]]
            elif version_pattern == '+1':
                matching_versions = [self.provider_latest_versions[provider]]
            else:
                matching_versions = fnmatch.filter(all_versions,
                                                   version_pattern)

            for version in matching_versions:
                box_list.append(self.provider_version_map[provider][version])

        return box_list

    def is_empty(self):
        """Check if the list of boxes is empty.

        Returns:
            bool: True if the list of boxes is empty.
        """
        return len(self.provider_version_map) == 0


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
