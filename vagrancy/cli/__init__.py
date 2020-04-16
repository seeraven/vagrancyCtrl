# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Command line interface used by vagrancyCtrl."""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import sys

import argcomplete

from .parser_cmd_delete   import get_subparser_delete
from .parser_cmd_download import get_subparser_download
from .parser_cmd_print    import get_subparser_print
from .parser_cmd_upload   import get_subparser_upload
from .parser_main         import get_main_parser


# -----------------------------------------------------------------------------
# Exported Functions
# -----------------------------------------------------------------------------

def get_parser():
    """Get the command line argument parser for vagrancyCtrl.

    Returns:
        argparse.ArgumentParser: A new ArgumentParser object of the parser.
    """
    parser = get_main_parser()
    subparsers = parser.add_subparsers()
    get_subparser_delete(subparsers)
    get_subparser_download(subparsers)
    get_subparser_print(subparsers)
    get_subparser_upload(subparsers)
    return parser


def vagrancy_ctrl_main():
    """Handle the vagrancyCtrl actions."""
    parser = get_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
