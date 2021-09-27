uttl.buildout
=============

Utilities for [zc.buildout](buildout.org/) as developed for *Up There They Love*.

# Usage

Add `uttl.buildout` to the `extensions` entry in your `[buildout]` section:

    [buildout]
    extensions = uttl.buildout

# Recipes

The following recipes (scripts) for `zc.buildout` are available in this package:

* [uttl.buildout.cmake](uttl/buildout/cmake/README.md) - Run CMake commands
* [uttl.buildout.copyfile](uttl/buildout/copyfile/README.md) - Copy files between directories
* [uttl.buildout.devenv](uttl/buildout/devenv/README.md) - Build projects with Visual Studio
* [uttl.buildout.dotnet.restore](uttl/buildout/dotnet/restore/README.md) - Restore .NET packages
* [uttl.buildout.inklecate](uttl/buildout/inklecate/README.md) - Compile .ink files to JSON
* [uttl.buildout.qmake](uttl/buildout/qmake/README.md) - Run QMake commands
* [uttl.buildout.qtdeploy](uttl/buildout/qtdeploy/README.md) - Deploy Qt libraries
* [uttl.buildout.versioncheck](uttl/buildout/versioncheck/README.md) - Get versioned executables

Check the source folders for detailed documentation about each command.

# Building from source

Check that you're running at least Python 3.9:

    D:\Projects\uttl-buildout>python --version
    Python 3.9.5

Build and install egg on system:

    python setup.py install

Create egg in `dist/` folder:

    python setup.py bdist_egg

Install manually:

    python -m easy_install -a dist\uttl_buildout-1.0.0-py3.9.egg

Upload to package manager:

    python -m twine upload --repository pypi dist/*
