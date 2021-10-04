uttl.buildout
=============

Utilities for [zc.buildout](buildout.org/) for different build systems on Windows, as used by [Up There They Love](https://uptheretheylove.com) for developing their titles.

# Usage

The `uttl.buildout` package will be automatically installed from [PyPi](https://pypi.org/project/uttl.buildout/) when you use it in your Buildout configuration.

You can also clone the repository to disk and use the recipes directly without installing a package:

    [buildout]
    develop = C:\Downloads\uttl-buildout

The downside of this approach is that your configuration will be invalidated (and thus your dependencies rebuilt) when the recipes change.

# Example

    [buildout]
    parts =
        visual-studio
        game

    # find installation for visual studio 2017

    [visual-studio]
    recipe = uttl.buildout:vswhere
    version = 2017

    # build game executable

    [game]
    recipe = uttl.buildout:devenv
    executable = ${visual-studio:product-path}
    solution = SSSG.sln
    project = SSSG
    build = Release

# Recipes

The following recipes (scripts) for `zc.buildout` are available in this package:

* [uttl.buildout.cmake](uttl/buildout/cmake/README.md) - Run CMake commands
* [uttl.buildout.command](uttl/buildout/README.md) - Run an executable with arguments
* [uttl.buildout.copyfile](uttl/buildout/copyfile/README.md) - Copy files between directories
* [uttl.buildout.devenv](uttl/buildout/devenv/README.md) - Build projects with Visual Studio
* [uttl.buildout.dotnet-restore](uttl/buildout/dotnet/restore/README.md) - Restore .NET packages using NuGet
* [uttl.buildout.inklecate](uttl/buildout/inklecate/README.md) - Compile .ink files to JSON
* [uttl.buildout.qmake](uttl/buildout/qmake/README.md) - Run QMake commands
* [uttl.buildout.qtdeploy](uttl/buildout/qtdeploy/README.md) - Deploy Qt libraries
* [uttl.buildout.versioncheck](uttl/buildout/versioncheck/README.md) - Get versioned executables
* [uttl.buildout.vswhere](uttl/buildout/vswhere/README.md) - Get Visual Studio installation paths

Check the source folders for detailed documentation about each recipe.

# Testing the package locally

Check that you're running at least Python 3.9:

    D:\Projects\uttl-buildout>python --version
    Python 3.9.5

Build and install egg on system:

    python setup.py install

# Uploading new package

Create egg in `dist/` folder:

    python setup.py bdist_egg

Upload packaged egg to repository:

    python -m twine upload --repository pypi dist/*
