Vagrancy CLI Control (vagrancyCtrl)
===================================

Synopsis
--------

vagrancyCtrl [-h|--help] [-u|--base-url BASE_URL] delete [-f|--force] [-p|--provider PROVIDER] BOX_NAME [VERSION]

vagrancyCtrl [-h|--help] [-u|--base-url BASE_URL] download OUTPUT_FILE BOX_NAME PROVIDER [VERSION]

vagrancyCtrl [-h|--help] [-u|--base-url BASE_URL] print [-p|--provider PROVIDER] [-v|--verbose] [--csv] [BOX_NAME]

vagrancyCtrl [-h|--help] [-u|--base-url BASE_URL] upload [-d|--delete-other-versions] INPUT_FILE BOX_NAME PROVIDER [VERSION]


Description
-----------

Vagrancy CLI Control (vagrancyCtrl) is a command line tool to manage boxes
stored in a vagrancy server. The following commands are available:

print
    To print the vagrant boxes on the vagrancy server, or to list all
    available versions of a certain box.

delete
    Delete vagrant boxes on the vagrancy server.

upload
    Upload a vagrant box to the vagrancy server.

download
    Download a vagrant box from the vagrancy server.


General Options
---------------

-h, --help                        Show the general help.
-u BASE_URL, --base-url BASE_URL  Specify the base URL of the vagrancy server. The default is either
                                  taken from the environment variable :code:`VAGRANY_URL` or the fixed
                                  value :code:`http://127.0.0.1:8099`.


The Subcommand print
--------------------

The subcommand :code:`print` displays all available boxes on the remote vagrancy server.
If given without the :code:`--verbose` option, it prints out only the box names. With the
:code:`--verbose` option, additional details such as the available version numbers are
shown.

The list of boxes to print can be limited by giving a :code:`BOX_NAME`. The :code:`BOX_NAME` is
actually a filename pattern that allows easy filtering of the boxes. In addition, a provider pattern
can be specified using the :code:`--provider` option to limit the shown boxes further.

The special option :code:`--csv` is intended for scripts or other programs to generate a
machine readable output.

-p PROVIDER, --provider PROVIDER  Print only boxes of the given pattern :code:`PROVIDER`. The string
                                  can contain wildcards such as :code:`*` and :code:`?`.
-v, --verbose                     Print details of each box, such as the latest version and the URLs
                                  for download and upload.
--csv                             Print a comma separated value list containing
			          boxname, provider, directory of the box in the vagrancy file store,
				  latest version, next version.


BOX_NAME
    The box or box pattern to print. The string can contain wildcards such
    as :code:`*` and :code:`?`.


The Subcommand delete
---------------------

The subcommand :code:`delete` deletes boxes from the vagrancy server. The command requires at least
a :code:`BOX_NAME` that is interpreted as a filename pattern. The boxes to delete can be further
filtered by using the :code:`--provider` option and/or by giving a :code:`VERSION`. The special
:code:`VERSION` value :code:`-1` selects all except the latest version.

The boxes are only deleted if the :code:`--force` option is given, otherwise the subcommand
only prints what boxes would be deleted.

-f, --force                       Delete the matching boxes. Otherwise matching boxes are only printed on stdout but no delete operation takes place.
-p PROVIDER, --provider PROVIDER  Only delete boxes that have the specified provider, e.g., libvirt or virtualbox.


BOX_NAME
    The box or box pattern to print. The string can contain wildcards such
    as :code:`*` and :code:`?`.

VERSION
    The version to delete. The string is interpreted as a shell pattern.
    Use :code:`*` to delete all versions or :code:`-1` to delete all but the latest version.


The Subcommand upload
---------------------

Upload a vagrant box to the vagrancy server. You have to specify the file, the
name of the vagrant box, the provider and the version of the box. If you want
to automatically generate a new version based on the latest version, you can
use :code:`-1` as the version specifier.

In addition, you can automatically delete all other versions of the vagrant box
on the vagrancy server by using the :code:`--delete-other-versions` option.
This is especially useful in combination with the automatic version number
generation to upload a new 'latest' version.


-d, --delete-other-versions  If specified, other versions of the vagrant box are deleted on the vagrancy server after uploading the new box.


INPUT_FILE
    The vagrant box file, usually a gzip tar archive.

BOX_NAME
    The vagrant box name. It must have a layout of :code:`<username>/<boxname>`.

PROVIDER
    The provider, e.g., libvirt or virtualbox.

VERSION
    The version of the vagrant box. The special value :code:`-1` allows you to automatically generate a version number based on the latest version.


The Subcommand download
-----------------------

Download a vagrant box from the vagrancy server. You have to specify the target
file, the name of the vagrant box, the provider and the version of the box. If
you specify the version as :code:`-1`, the latest version is automatically determined
and downloaded.


OUTPUT_FILE
    The target file name of the vagrant box file. Specify '-' to write the file to stdout.

BOX_NAME
    The vagrant box name.

PROVIDER
    The provider, e.g., libvirt or virtualbox.

VERSION
    The version of the vagrant box. The special value :code:`-1` allows you to automatically select the latest version.


Environment
-----------

:code:`VAGRANCY_URL` defines the default vagrancy server URL.


License
-------

vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl) is released under the
"BSD 3-Clause License". Please see the LICENSE file that is included as part of this package.
