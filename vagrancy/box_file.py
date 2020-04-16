# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""
Representation of a specific box file.

This module specifies the class :class:`BoxFile` that represents a specific box
identified by a name, at a specific version and for a specific provider.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import os
import sys

import requests


# -----------------------------------------------------------------------------
# Class Definitions
# -----------------------------------------------------------------------------
class BoxFile:
    """Representation of a specific box.

    This class represents a specific box identified by a name, with a specific
    version and a specific provider.

    Attributes:
        _server_url (str): The vagrancy server base URL.
        box_name (str):    The box name confirming to ``<username>/<name>``.
        version (str):     The version of the box.
        provider (str):    The provider, e.g., ``virtualbox``.
    """

    def __init__(self, server_url, box_name, version, provider):
        """Create a new Box object.

        Args:
            server_url (str): The base URL of the vagrancy server.
            box_name (str):   The box name confirming to ``<username>/<name>``.
            version (str):    The version of the box.
            provider (str):   The provider, e.g., ``virtualbox``.

        Raises:
            ValueError: If the `box_name` does not confirm to ``<username>/<name>``.
        """
        self._server_url = server_url
        self.box_name = box_name
        self.version = version
        self.provider = provider

        if self.box_name.count('/') != 1:
            raise ValueError("The argument box_name must contain exactly one '/'!")

    def get_url(self):
        """Get the URL of the box.

        Returns:
            str: The URL of the box.
        """
        url = "%s/%s/%s/%s" % (self._server_url, self.box_name, self.version, self.provider)
        return url

    def upload(self, box_file):
        """Upload a box file.

        Args:
            box_file (str):   The path to the box file to upload.

        Returns:
            bool: Returns True on success, otherwise False.

        Raises:
            requests.exceptions.ConnectionError: Raised if the base URL can
                not be reached.
        """
        url = self.get_url()
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        with open(box_file, 'rb') as payload:
            response = requests.put(url, data=payload, headers=headers)

        return response.status_code == 201

    def download(self, box_file):
        """Download a box file.

        Args:
            box_file (str):   The path to the box file to upload.

        Returns:
            bool: Returns True on success, otherwise False.

        Raises:
            requests.exceptions.ConnectionError: Raised if the base URL can
                not be reached.
        """
        url = self.get_url()
        response = requests.get(url, stream=True)

        if box_file == '-':
            for chunk in response:
                os.write(sys.stdout.fileno(), chunk)
        else:
            with open(box_file, 'wb') as payload:
                for chunk in response:
                    payload.write(chunk)

        return response.status_code == 200

    def delete(self):
        """Delete the box.

        Returns:
            bool: Returns True on success, otherwise False.

        Raises:
            requests.exceptions.ConnectionError: Raised if the base URL can
                not be reached.
        """
        url = self.get_url()
        response = requests.delete(url)
        return response.status_code == 200


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
