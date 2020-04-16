# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Main CLI parser of vagrancyCtrl.

Attributes:
    DESCRIPTION (str): The usage description of the main parser.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import argparse
import os


# -----------------------------------------------------------------------------
# Module Variables
# -----------------------------------------------------------------------------
DESCRIPTION = """
Interface with a vagrancy server to manage vagrant boxes. The following commands
are available:
 - print    : To print the vagrant boxes on the vagrancy server, or to list all
              available versions of a certain box.
 - delete   : Delete vagrant boxes on the vagrancy server.
 - upload   : Upload a vagrant box to the vagrancy server.
 - download : Download a vagrant box from the vagrancy server.

Return codes:
 0 - Communication was successfull.
 1 - Communication failed.
"""


# -----------------------------------------------------------------------------
# Exported Functions
# -----------------------------------------------------------------------------

def get_main_parser():
    """Return the main parser.

    Returns:
        argparse.ArgumentParser: A new ArgumentParser object of the parser.
    """
    parser = argparse.ArgumentParser(description = DESCRIPTION,
                                     formatter_class = argparse.RawTextHelpFormatter)

    # General options
    parser.add_argument("-u", "--base-url",
                        help = "Base URL of vagrancy. Default: %(default)s",
                        action = "store",
                        default = os.getenv('VAGRANCY_URL', 'http://127.0.0.1:8099'))

    return parser


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
