# uttl.buildout.versioncheck

Finds the path to an installed executable and checks whether its semantic version number meets the required major and minor version number.

You will need to write a custom script function that retrieves a version number for the executable you are looking for. This means that the recipe is not limited to a specific type of executable. As long as you can compare version numbers, you can use it to get to path to anything installed on the system.

The recipe will fail and throw an error if the installed version is lower than the required one.

Semantic versioning means that you have a major, minor, and debug version number for an executable that is written as `<major>.<minor>.<debug>`. Most applications use this scheme, or something similar, but not all.

Even when a semantic version does not exist you can still create your own. For example, you can say that the semantic version number for a version of Visual Studio is `2017.15.64`. 2017 is the major version of the program, but it's known internally as version 15 (minor) and you want the 64-bit version (debug).

The path to the executable and its version number are cached in a .ini file in the `\parts` directory.

## Options

`body` (required)

Script function written in Python that is run to get the path to an executable. Lines of the function must be prefixed with `...` and must always return a tuple of values in this format: (Success (`True` or `False`), MajorVersion (`int`), MinorVersion (`int`), DebugVersion (`int`), Path (`string`)). The function can reference any option defined in the configuration using `self.options` and can write messages to the log using `self.log`.

`required-major` (default: 0)

Minimum requirement for the major version of the executable. Can be 0.

`required-minor` (default: 0)

Minimum requirement for the minor version of the executable. Can be 0.

`version-file` (default: "<name>.ini")

Name for the .ini cache file in the `\parts` directory. Will default to the name of the buildout section.

## Outputs

`path`

Path to the found executable.

`version-major`

Major version number of the executable.

`version-minor`

Minor version number of the executable.

`version-debug`

Debug version number of the executable.

## Example - Get the path to Visual Studio 2017

    [visual-studio]
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
        ... return (True, self.options['required-major'], self.options['required-minor'], 64, path)

## Example - Find CMake and set the generator to Visual Studio 2017

	[cmake]
	recipe = uttl.buildout:versioncheck
	required-major = 3
	required-minor = 19
	generator = Visual Studio ${visual-studio:version-minor} ${visual-studio:version-major} Win${visual-studio:version-debug}
	body = ... import winreg
		...
		... try:
		...   key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Kitware\CMake', 0, winreg.KEY_READ)
		...   installed = winreg.QueryValueEx(key, 'installed')
		... except OSError:
		...   self.log.error('CMake is not installed.')
		...   return (False, 0, 0, 0, '')
		...  
		... if installed[0] != 1:
		...   self.log.error('CMake is not installed.')
		...   return (False, 0, 0, 0, '')
		...
		... version_full = None
		...
		... try:
		...   p = subprocess.Popen([ 'cmake', '--version' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		... except FileNotFoundError:
		...   self.log.error('CMake was not added to the global path environment variable.')
		...   return (False, 0, 0, 0, '')
		...
		... for line in iter(p.stdout.readline, b''):
		...   match = re.match('.*version ([0-9]+\\.[0-9]+\\.[0-9]+)', str(line))
		...   if match:
		...     version_full = match.group(1)
		...     break
		...
		... if not version_full:
		...   self.log.error('Failed to determine CMake version.')
		...   return (False, 0, 0, 0, '')
		...
		... match = re.match(r'([0-9]+)\.([0-9]+)\.([0-9]+)', version_full)
		... if not match:
		...   self.log.error('Incorrect format for version: "%s".' % (version_full))
		...   return (False, 0, 0, 0, '')
		...
		... return (True, match.group(1), match.group(2), match.group(3), 'cmake')