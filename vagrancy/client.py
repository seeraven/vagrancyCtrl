# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""
Client for accessing a vagrancy server.

This module specifies the client class :class:`Vagrancy` to access a vagrancy
server.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import fnmatch

import requests

from .box import Box


# -----------------------------------------------------------------------------
# Class Definitions
# -----------------------------------------------------------------------------
class Vagrancy:
    """This class represents an interface to a Vagrancy server."""

    def __init__(self, server_url):
        """Create a new Vagrancy object using the specified base URL.

        Args:
            server_url (str): The base URL of the vagrancy.
        """
        self._server_url = server_url

    def get_boxes(self, pattern = '*', provider_pattern = '*'):
        """Get a list of all available boxes.

        Args:
            pattern (str): A file name pattern to limit the boxes to
            return.
            provider_pattern (str): A pattern to limit the boxes to
            return to include only the matching providers.

        Returns:
            list: A list of all available boxes as Box objects.

        Raises:
            ConnectionRefusedError: Raised if the remote URL has no
                ``/inventory`` API hook.
            requests.exceptions.ConnectionError: Raised if the base URL can
                not be reached.
        """
        boxes = []
        filtered_box_names = fnmatch.filter(self.inventory(), pattern)
        for box_name in filtered_box_names:
            box = Box(self._server_url, box_name, provider_pattern)

            if not box.is_empty():
                boxes.append(box)

        return boxes

    def inventory(self):
        """Get a list of all available boxes.

        Returns:
            list: A list of all available boxes.

        Raises:
            ConnectionRefusedError: Raised if the remote URL has no
                ``/inventory`` API hook.
            requests.exceptions.ConnectionError: Raised if the base URL can
                not be reached.
        """
        response = requests.get("%s/inventory" % self._server_url)
        if response.status_code == 404:
            raise ConnectionRefusedError("Vagrancy server at %s does not support "
                                         "the /inventory API hook!" % self._server_url)

        response_data = response.json()
        if 'boxes' not in response_data:
            return []

        return response_data['boxes']


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
