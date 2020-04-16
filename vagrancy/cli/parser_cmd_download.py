# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Parser of the download command of vagrancyCtrl.

Attributes:
    DESCRIPTION (str): The usage description of the subparser for the download command.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import argparse
import sys

from ..client import Vagrancy


# -----------------------------------------------------------------------------
# Module Variables
# -----------------------------------------------------------------------------
DESCRIPTION = """
Download a vagrant box from the vagrancy server. You have to specify the target
file, the name of the vagrant box, the provider and the version of the box. If
you specify the version as '-1', the latest version is automatically determined
and downloaded.


Return codes:
 0 - Communication was successfull.
 1 - Communication failed.
"""


# -----------------------------------------------------------------------------
# Exported Functions
# -----------------------------------------------------------------------------

def exec_download_cmd(args):
    """Execute the download command.

    Args:
        args: The arguments object.
    """
    vagrancy = Vagrancy(args.base_url)

    box_list = vagrancy.get_boxes(args.box_name, args.provider)
    if len(box_list) == 0:
        print("ERROR: Found no matching boxes!")
        sys.exit(1)
    elif len(box_list) > 1:
        print("ERROR: Found %d matching boxes! Please provide a unique name/pattern!" %
              len(box_list))
        sys.exit(1)

    version_pattern = args.version
    if version_pattern == "-1":
        version_pattern = "+1"
    box_files = box_list[0].get_filtered_box_files(version_pattern, args.provider)

    if len(box_files) == 0:
        print("ERROR: Found no matching box files for the specified provider/version pattern!")
        sys.exit(1)
    elif len(box_files) > 1:
        print("ERROR: Found %d matching boxes for the specified provider/version!" % len(box_files))
        print("       Please use a unique name/pattern!")
        sys.exit(1)

    if box_files[0].download(args.output_file):
        if args.output_file != '-':
            print("Downloaded vagrant box %s (provider %s, version %s) "
                  "successfully." % (box_files[0].box_name,
                                     box_files[0].provider,
                                     box_files[0].version))
        sys.exit(0)

    print("ERROR: Download of box %s (provider %s, version %s) failed!" % (box_files[0].box_name,
                                                                           box_files[0].provider,
                                                                           box_files[0].version))
    sys.exit(1)


def get_subparser_download(subparsers):
    """Return the subparser to configure and handle the download command.

    Args:
        subparsers: The subparsers object of the main argparse.ArgumentParser.

    Returns:
        argparse.ArgumentParser: The new subparser object.
    """
    parser_download = subparsers.add_parser("download",
                                            help = "Download a vagrant box.",
                                            description = DESCRIPTION,
                                            formatter_class = argparse.RawTextHelpFormatter)
    parser_download.add_argument("output_file",
                                 action = "store",
                                 help = "The target file name of the vagrant "
                                 "box file. Specify '-' to write the file to "
                                 "stdout.")
    parser_download.add_argument("box_name",
                                 action = "store",
                                 help = "The vagrant box name.")
    parser_download.add_argument("provider",
                                 action = "store",
                                 help = "The provider, e.g., libvirt or "
                                 "virtualbox.")
    parser_download.add_argument("version",
                                 action = "store",
                                 help = "The version of the vagrant box. The "
                                 "special value '-1' allows you to automatically "
                                 "select the latest version. Default: %(default)s",
                                 default = "-1",
                                 nargs = "?")
    parser_download.set_defaults(func = exec_download_cmd)
    return parser_download


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
