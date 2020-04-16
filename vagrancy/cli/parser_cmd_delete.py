# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Parser of the delete command of vagrancyCtrl.

Attributes:
    DESCRIPTION (str): The usage description of the subparser for the delete command.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import argparse
import sys

from ..client   import Vagrancy


# -----------------------------------------------------------------------------
# Module Variables
# -----------------------------------------------------------------------------
DESCRIPTION = """
Delete matching vagrant boxes from the vagrancy server. The box to delete
must be specified as an argument, e.g., as:
 %(prog)s base/ubuntu-14.04.5-server-armv7-daily_pkgbuildbox

To delete only a certain version of the box, you can specify a pattern as
the second argument. This pattern is matched with all found versions of the
box and only matching versions are deleted. The special version '-1' can be
used to match all but the latest version:
 %(prog)s base/ubuntu-14.04.5-server-armv7-daily_pkgbuildbox -1

Like the print command, you can specifiy a provider using the '--provider'
option to limit the deletion to the specified provider.

Please note that the deletion is only performed when you specify the '--force'
option. Otherwise, only the matching URLs are printed. This is a precaution to
avoid unintentional deletion.

Return codes:
 0 - Communication was successfull.
 1 - Communication failed.
"""


# -----------------------------------------------------------------------------
# Exported Functions
# -----------------------------------------------------------------------------

def exec_delete_cmd(args):
    """Execute the delete command.

    Args:
        args: The arguments object.
    """
    vagrancy = Vagrancy(args.base_url)

    box_list = vagrancy.get_boxes(args.box_name, args.provider)
    if len(box_list) == 0:
        print("ERROR: Found no matching boxes!")
        sys.exit(1)

    for box in box_list:
        box_files = box.get_filtered_box_files(args.version, args.provider)
        for box_file in box_files:
            if args.force:
                if not box_file.delete():
                    print("ERROR: Delete of box %s (provider %s, version %s) failed!" %
                          (box_file.box_name, box_file.provider, box_file.version))
                    sys.exit(1)
                print("INFO: Deleted box %s (provider %s, version %s)"  %
                      (box_file.box_name, box_file.provider, box_file.version))
            else:
                print("INFO: Would delete box %s (provider %s, version %s)"  %
                      (box_file.box_name, box_file.provider, box_file.version))

    sys.exit(0)


def get_subparser_delete(subparsers):
    """Return the subparser to configure and handle the delete command.

    Args:
        subparsers: The subparsers object of the main argparse.ArgumentParser.

    Returns:
        argparse.ArgumentParser: The new subparser object.
    """
    parser_delete = subparsers.add_parser("delete",
                                          help = "Delete a vagrant box.",
                                          description = DESCRIPTION,
                                          formatter_class = argparse.RawTextHelpFormatter)
    parser_delete.add_argument("-f", "--force",
                               action = "store_true",
                               help = "Delete the matching boxes. Otherwise "
                               "matching boxes are only printed on stdout but "
                               "no delete operation takes place.",
                               default = False)
    parser_delete.add_argument("-p", "--provider",
                               action = "store",
                               help = "Only delete boxes that have the specified "
                               "provider, e.g., libvirt or virtualbox.",
                               default = "*")
    parser_delete.add_argument("box_name",
                               action = "store",
                               help = "The vagrant box name pattern. A box name must have "
                               "a layout of <username>/<boxname>. Default: %(default)s",
                               default = "*")
    parser_delete.add_argument("version",
                               action  = "store",
                               help = "The version to delete. The string is "
                               "interpreted as a shell pattern. Use '*' to delete "
                               "all versions or '-1' to delete all but the latest "
                               "version. Default: %(default)s",
                               default = "*",
                               nargs = "?")
    parser_delete.set_defaults(func = exec_delete_cmd)
    return parser_delete


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
