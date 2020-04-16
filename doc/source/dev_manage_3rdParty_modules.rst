Manage 3rd party Modules
------------------------

Including 3rd party modules ensures that this applications has all dependencies
included and does not rely on system packages. This blows up the package size
but makes it much easier to port the application.

The modules are stored in the :code:`src/share/vagrancyCtrl/modules/3rdParty` directory.
To make updating and installation more easy, the script
:code:`devtools/3rdParty_Modules/update3rdParty.sh` was written that updates all
modules configured in the file :code:`devtools/3rdParty_Modules/modules.conf`. Here
you can add your additional modules and configure the version of the modules.
