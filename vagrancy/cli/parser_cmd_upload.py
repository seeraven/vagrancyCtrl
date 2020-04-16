# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
#
"""Parser of the upload command of vagrancyCtrl.

Attributes:
    DESCRIPTION (str): The usage description of the subparser for the upload command.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import argparse
import sys

from ..box_file import BoxFile
from ..client   import Vagrancy


# -----------------------------------------------------------------------------
# Module Variables
# -----------------------------------------------------------------------------
DESCRIPTION = """
Upload a vagrant box to the vagrancy server. You have to specify the file, the
name of the vagrant box, the provider and the version of the box. If you want
to automatically generate a new version based on the latest version, you can
use '-1' as the version specifier.

In addition, you can automatically delete all other versions of the vagrant box
on the vagrancy server. This is especially useful in combination with the
automatic version number generation to upload a new 'latest' version.


Return codes:
 0 - Communication was successfull.
 1 - Communication failed.
"""


# -----------------------------------------------------------------------------
# Exported Functions
# -----------------------------------------------------------------------------

def exec_upload_cmd(args):
    """Execute the upload command.

    Args:
        args: The arguments object.
    """
    if '*' in args.provider or '?' in args.provider:
        print("ERROR: Please do not use a pattern for the provider!")
        sys.exit(1)

    vagrancy = Vagrancy(args.base_url)

    box_list = vagrancy.get_boxes(args.box_name, args.provider)
    if len(box_list) > 1:
        print("ERROR: Found %d matching boxes! Please provide a unique name/pattern!" %
              len(box_list))
        sys.exit(1)

    if len(box_list) == 0:
        # The box file does not exist yet
        if args.version == '-1':
            args.version = '1.0.0'
        box_file = BoxFile(args.base_url, args.box_name, args.version, args.provider)
        if not box_file.upload(args.input_file):
            print("ERROR: Upload of box %s (provider %s, version %s) failed!" % (box_file.box_name,
                                                                                 box_file.provider,
                                                                                 box_file.version))
            sys.exit(1)

        print("INFO: Uploaded box %s (provider %s, version %s) successfully." % (box_file.box_name,
                                                                                 box_file.provider,
                                                                                 box_file.version))
        sys.exit(0)

    # Check if we have to determine the new version
    if args.version == '-1':
        args.version = box_list[0].provider_next_versions[args.provider]

        if args.version is None:
            print("ERROR: New version of box %s (provider %s) can not be "
                  "determined!" % (box_list[0].box_name,
                                   args.provider))
            print("       Probably the box uses a non-semantic versioning!")
            print("       Please specify the version!")
            sys.exit(1)

        print("INFO: New version of box %s (provider %s) determined as %s." % (box_list[0].box_name,
                                                                               args.provider,
                                                                               args.version))

    # Upload the box
    box_file = BoxFile(args.base_url, box_list[0].box_name, args.version, args.provider)
    if not box_file.upload(args.input_file):
        print("ERROR: Upload of box %s (provider %s, version %s) failed!" % (box_file.box_name,
                                                                             box_file.provider,
                                                                             box_file.version))
        sys.exit(1)

    print("INFO: Uploaded box %s (provider %s, version %s) successfully." % (box_file.box_name,
                                                                             box_file.provider,
                                                                             box_file.version))

    if args.delete_other_versions:
        box_list[0].retrieve_box_data(args.provider)
        all_old_box_files = box_list[0].get_filtered_box_files(version_pattern='-1')
        delete_success = True

        if all_old_box_files:
            print("INFO: Deleting %d old box files..." % len(all_old_box_files))
            for box_file in all_old_box_files:
                if box_file.delete():
                    print("INFO:  Deleted version %s successfully." % box_file.version)
                else:
                    print("ERROR: Can't delete version %s!" % box_file.version)
                    delete_success = False
        else:
            print("INFO: No old box files to delete.")

        if not delete_success:
            sys.exit(1)

    sys.exit(0)


def get_subparser_upload(subparsers):
    """Return the subparser to configure and handle the upload command.

    Args:
        subparsers: The subparsers object of the main argparse.ArgumentParser.

    Returns:
        argparse.ArgumentParser: The new subparser object.
    """
    parser_upload = subparsers.add_parser("upload",
                                          help = "Upload a vagrant box.",
                                          description = DESCRIPTION,
                                          formatter_class = argparse.RawTextHelpFormatter)
    parser_upload.add_argument("-d", "--delete-other-versions",
                               action  = "store_true",
                               help = "If specified, other versions of the "
                               "vagrant box are deleted on the vagrancy server "
                               "after uploading the new box.",
                               default = False)
    parser_upload.add_argument("input_file",
                               action  = "store",
                               help = "The vagrant box file, usually a gzip tar "
                               "archive.")
    parser_upload.add_argument("box_name",
                               action = "store",
                               help = "The vagrant box name. It must have "
                               "a layout of <username>/<boxname>.")
    parser_upload.add_argument("provider",
                               action = "store",
                               help = "The provider, e.g., libvirt or "
                               "virtualbox.")
    parser_upload.add_argument("version",
                               action = "store",
                               help = "The version of the vagrant box. The "
                               "special value '-1' allows you to automatically "
                               "generate a version number based on the latest "
                               "version. Default: %(default)s",
                               default = "-1",
                               nargs = "?")
    parser_upload.set_defaults(func = exec_upload_cmd)
    return parser_upload


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
