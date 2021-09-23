# uttl.buildout.versioncheck

Recipe for finding the path to an executable and checking its version against a required one using a Python function.

The resulting path and version number is written to an ini file in the `parts` directory. The script function is called if the ini file does not exist. The output of the found version information is checked against the values stored in the cache during the `install` phase of the recipe. VersionCheck will always fail if the requested version cannot be found.

## Configuration

``body`` (required)

Python script function that is ran to get the path to an executable. Lines of the function must be prefixed with `...`. The function must always return a tuple of values in this format: (Success (`True` or `False`), MajorVersion (`int`), MinorVersion (`int`), DebugVersion (`int`), Path (`string`)).

``required_major`` (default: 0)

Minimum requirement for the major version of the executable. Can be 0.

``required_minor`` (default: 0)

Minimum requirement for the minor version of the executable. Can be 0.

``required_debug`` (default: 0)

Minimum requirement for the debug version of the executable. Not taken into consideration when comparing versions.

``version_file`` (default: "<name>.ini")

Override for the name of the ini file in the parts directory.

## Outputs

``path``

  Path to the found executable.

``version_major``

  Major version number of the executable.

``version_minor``

  Minor version number of the executable.

``version_debug``

  Debug version number of the executable.

## Example

Using `vswhere.exe` to get the path to Visual Studio 2017 (version 15):

    [visual-studio]
    recipe = uttl.buildout:versioncheck
    required_major = 2017
    required_minor = 15
    body = ... path = None
        ... args = [ 
        ...   r'%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe',
        ...   '-version',
        ...   '%s.0' % (self.options['required_minor']),
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
        ... return (True, self.options['required_major'], self.options['required_minor'], 64, path)
