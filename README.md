             ___   _____        __  __    __       
     /\ /\  / _ \ /__   \/\  /\/__\/__\  /__\      
    / / \ \/ /_)/   / /\/ /_/ /_\ / \// /_\        
    \ \_/ / ___/   / / / __  //__/ _  \//__        
     \___/\/       \/  \/ /_/\__/\/ \_/\__/        
                                                   
     _____        __          __    ___         __ 
    /__   \/\  /\/__\/\_/\   / /   /___\/\   /\/__\
      / /\/ /_/ /_\  \_ _/  / /   //  //\ \ / /_\  
     / / / __  //__   / \  / /___/ \_//  \ V //__  
     \/  \/ /_/\__/   \_/  \____/\___/    \_/\__/  

Utilities for [buildout](buildout.org/) as developed for *Up There They Love*.

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

# VersionCheck

Recipe for finding the path to an executable and checking its version against a required one by using Python scripting. The resulting path and version number is written to an ini file in your parts directory. The script function will always be called and its output is checked against the values stored in the cache.

## Options

``body`` (required)

  Python script function that is ran to get the path to an executable. Lines of the function must be prefixed with `...`. The function must always return a tuple of values in this format: `(Success (True or False), MajorVersion (int), MinorVersion (int), DebugVersion (int), Path (string))`.

``required_major`` (default: 0)

  Minimum requirement for the major version of the executable. Can be 0.

``required_minor`` (default: 0)

  Minimum requirement for the minor version of the executable. Can be 0.

``required_debug`` (default: 0)

  Minimum requirement for the debug version of the executable. Not taken into consideration when comparing versions.

``version_file`` (default: "<name>.ini")

  Override for the name of the ini file in the parts directory.

## Example

Using `vswhere.exe` to get the path to Visual Studio:

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