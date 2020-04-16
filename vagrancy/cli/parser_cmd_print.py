# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Parser of the print command of vagrancyCtrl.

Attributes:
    DESCRIPTION (str): The usage description of the subparser for the print command.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import argparse
import os
import sys

from ..client   import Vagrancy


# -----------------------------------------------------------------------------
# Module Variables
# -----------------------------------------------------------------------------
DESCRIPTION = """
Get a list of all available boxes on the vagrancy server. Without any arguments,
the names of all boxes are printed:
  %(prog)s

You can also limit the list by specifiing a pattern:
  %(prog)s base/*18.04*

Using the '--provider' option, you can limit the output list to a certain
provider (virtualbox, libvirt), e.g., by listing only virtualbox images:
  %(prog)s --provider virtualbox

To get more information about the boxes, such as the provider, versions, etc.,
you can use the '--verbose' option:
  %(prog)s --verbose base/*18.04*

To use the information in a script, you can specifiy the '--cvs' option to get
a comma separated list consisting of:
 - name of box on vagrancy
 - provider
 - directory to the box file relative to the vagrancy file store
 - latest version
 - next version


Return codes:
 0 - Communication was successfull.
 1 - Communication failed.
"""


# -----------------------------------------------------------------------------
# Exported Functions
# -----------------------------------------------------------------------------

def exec_print_cmd(args):
    """Execute the print command.

    Args:
        args: The arguments object.
    """
    vagrancy = Vagrancy(args.base_url)
    box_list = vagrancy.get_boxes(args.box_name, args.provider)

    if args.csv:
        for box in box_list:
            for provider in sorted(box.provider_version_map.keys()):
                latest_version   = box.provider_latest_versions[provider]
                next_version     = box.provider_next_versions[provider]

                if next_version is None:
                    next_version = ''

                print("%s,%s,%s,%s,%s" % (box.box_name, provider,
                                          os.path.join(box.box_name, latest_version, provider),
                                          latest_version, next_version))
        sys.exit(0)

    if args.verbose:
        for box in box_list:
            print("%s:" % box.box_name)

            for provider in sorted(box.provider_version_map.keys()):
                latest_version   = box.provider_latest_versions[provider]
                next_version     = box.provider_next_versions[provider]

                if next_version is None:
                    next_version = 'undefined'

                print(" Provider:           %s" % provider)
                print(" Available Versions: %s" % ' '.join(sorted(box.version_provider_map.keys())))
                print(" Latest Version:     %s" % latest_version)
                print(" Next Version:       %s" % next_version)
                print(" Download URL:       %s" % os.path.join(args.base_url,
                                                               box.box_name,
                                                               latest_version,
                                                               provider))
                print(" Upload URL:         %s" % os.path.join(args.base_url,
                                                               box.box_name,
                                                               next_version,
                                                               provider))
                print()

        sys.exit(0)

    for box in box_list:
        print("%s" % box.box_name)


def get_subparser_print(subparsers):
    """Return the subparser to configure and handle the print command.

    Args:
        subparsers: The subparsers object of the main argparse.ArgumentParser.

    Returns:
        argparse.ArgumentParser: The new subparser object.
    """
    parser_print = subparsers.add_parser("print",
                                         help = "Print the contents of the vacrancy server.",
                                         description = DESCRIPTION,
                                         formatter_class = argparse.RawTextHelpFormatter)

    parser_print.add_argument("-p", "--provider",
                              action = "store",
                              help = "Only print boxes that have the specified "
                              "provider, e.g., libvirt or virtualbox.",
                              default = "*")
    parser_print.add_argument("-v", "--verbose",
                              action = "store_true",
                              help = "Be verbose and print all available "
                              "information about the boxes.",
                              default = False)
    parser_print.add_argument("--csv",
                              action = "store_true",
                              help = "Print a csv list instead of only the names.",
                              default = False)
    parser_print.add_argument("box_name",
                              action = "store",
                              help = "Print only names that match the given "
                              "pattern. Default: %(default)s",
                              default = "*",
                              nargs   = "?")
    parser_print.set_defaults(func = exec_print_cmd)
    return parser_print


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
