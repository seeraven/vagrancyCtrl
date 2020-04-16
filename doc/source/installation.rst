Installation
============

The following installation methods are provided:

* a pip package
* a debian package
* a self-contained executable generated using PyInstaller_


Installation as a Pip Package
-----------------------------

Installation as a pip package is done by calling::

    $ pip install vagrancyCtrl


Installation as a Debian Package
--------------------------------    

Installation of the debian package is the preferred way of installing
vagrancyCtrl on debian based distributions like Ubuntu::

    $ wget https://github.com/seeraven/vagrancyCtrl/releases/...
    $ sudo dpkg -i vagrancyCtrl-*.deb


Installation as the Self-Contained Executable
---------------------------------------------

Installation of the self-contained executable allows you to install
vagrancyCtrl on systems even if they do not provide python themselfes.
However, the usage of vagrancyCtrl is limited to the command line tool
itself, so the integration in other scripts won't be possible::

    $ wget https://github.com/seeraven/vagrancyCtrl/releases/...
    $ mv .. /usr/local/bin/vagrancyCtrl
    $ chmod +x /usr/local/bin/vagrancyCtrl


.. _PyInstaller: http://www.pyinstaller.org/
