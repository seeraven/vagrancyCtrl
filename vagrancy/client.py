"""
Client for accessing a vagrancy server.

Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
All rights reserved.
This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl) and
is released under the "BSD 3-Clause License". Please see the LICENSE file that
is included as part of this package.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import requests


# -----------------------------------------------------------------------------
# Class Definitions
# -----------------------------------------------------------------------------
class Vagrancy:
    """This class represents an interface to a Vagrancy server."""

    def __init__(self, server_url):
        """Create a new Vagrancy object using the specified base URL."""
        self._server_url = server_url

    def inventory(self):
        """Get a list of all available boxes."""
        response = requests.get("%s/inventory" % self._server_url)
        if response.status_code == 404:
            raise ConnectionRefusedError("Vagrancy server at %s does not support "
                                         "the /inventory API hook!")
        return response.json()['boxes']

    def upload(self):
        """Upload a box."""
        print("Do something on %s" % self._server_url)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
