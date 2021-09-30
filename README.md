uttl.buildout
=============

Utilities for [zc.buildout](buildout.org/) for different build systems on Windows, as used by [Up There They Love](https://uptheretheylove.com) for developing their titles.

# Usage

The `uttl.buildout` package will be automatically installed from [PyPi](https://pypi.org/project/uttl.buildout/) using `easy_install` when you use it in your buildout configuration.

You can also clone the repository to disk and use the recipes directly without installing a package.

    [buildout]
    develop = C:\Downloads\uttl-buildout

The downside of this approach is that your configuration will be invalidated (and thus your dependencies rebuilt) when the recipes change.

# Example

    [buildout]
    parts =
        devenv
        game

    # find devenv executable from visual studio path

    [devenv]
    recipe = uttl.buildout:versioncheck
    required-major = 2017
    required-minor = 15
    body = ... path = None
        ... args = [ 
        ...   r'%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe',
        ...   '-version',
        ...   '%s.0' % (self.options['required-minor']),
        ...   '-property',
        ...   'installationPath'
        ... ]
        ...
        ... try:
        ...   with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        ...     for line in iter(proc.stdout.readline, b''):
        ...       path = os.path.abspath(str(line.rstrip(), encoding='ascii'))
        ...       break
        ... except FileNotFoundError:
        ...   self.log.error('Visual Studio is not installed.')
        ...   return (False, 0, 0, 0, '')
        ...
        ... if not path:
        ...   self.log.error('Cannot find Visual Studio executable.')
        ...   return (False, 0, 0, 0, '')
        ...
        ... path = os.path.abspath(path + r'\Common7\IDE\devenv.com')
        ... if not os.path.exists(path):
        ...   self.log.error('Failed to find path to devenv.')
        ...   return (False, 0, 0, 0, '')
        ...
        ... return (True, self.options['required-major'], self.options['required-minor'], 64, path)

    # build game executable

    [game]
    recipe = uttl.buildout:devenv
    executable = ${devenv:path}
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

Check the source folders for detailed documentation about each recipe.

# Building from source

Check that you're running at least Python 3.9:

    D:\Projects\uttl-buildout>python --version
    Python 3.9.5

Build and install egg on system:

    python setup.py install

Create egg in `dist/` folder:

    python setup.py bdist_egg

Install on your system using `easy_install`:

    python -m easy_install -a dist\uttl_buildout-1.0.0-py3.9.egg

Upload packaged egg to repository:

    python -m twine upload --repository pypi dist/*
