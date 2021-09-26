uttl.buildout
=============

Utilities for [zc.buildout](buildout.org/) as developed for *Up There They Love*.

# Building from source

Check that you're running at least Python 3.9:

    D:\Projects\uttl-buildout>python --version
    Python 3.9.5

Build and install egg:

    python setup.py install

Create egg and install manually:

    python setup.py bdist_egg
    python -m easy_install -a dist\uttl_buildout-1.0.0-py3.9.egg

# Usage

Add `uttl.buildout` to the `extensions` entry in your `[buildout]` section:

    [buildout]
    extensions = uttl.buildout

# Recipes

The following recipes (scripts) for `zc.buildout` are available in this package:

* [uttl.buildout.cmake](uttl/buildout/cmake/README.md) - Run CMake commands
* `uttl.buildout.copyfile`
* `uttl.buildout.devenv`
* `uttl.buildout.dotnet`
* [uttl.buildout.inklecate](uttl/buildout/inklecate/README.md) - Compile .ink files to JSON
* [uttl.buildout.qmake](uttl/buildout/qmake/README.md) - Run QMake commands
* [uttl.buildout.qtdeploy](uttl/buildout/qtdeploy/README.md) - Deploy Qt libraries
* [uttl.buildout.versioncheck](uttl/buildout/versioncheck/README.md) - Get versioned executables

Check the source folders for detailed documentation about each command.