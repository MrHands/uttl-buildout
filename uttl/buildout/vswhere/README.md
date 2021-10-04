# uttl.buildout.vswhere

Recipe for retrieving the installation path to Visual Studio using Microsoft's `vswhere` tool.

## Options

`executable` (default: "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe")

Path to the executable used to run commands. While the executable should be installed on your system with a newer version of Visual Studio, you can still opt to use a version that is installed locally.

`version` (required)

Version of Visual Studio that you want to retrieve. Can be a product number (e.g. 2017), a tools number (e.g. 10), or "latest". An error will be raised if the requested version could not be found or if the installed version is not sufficient.

## Outputs

`display-name`

Full name for the product, e.g. "Visual Studio Community 2017".

`version-product`

Version number for the product, e.g. "2019" for Visual Studio 2019.

`version-tools`

Version number for the tools, e.g. "9" for Visual Studio 2008.

`install-dir`

Path to the Visual Studio installation directory.

`tool-path`

Path to the executable used for running Visual Studio commands.

`vcvars-path`

Path to the `vcvarsall.bat` batch script for setting up the Visual Studio environment on the command-line.

## Example - Set up generator for CMake based on Visual Studio version

	[visual-studio]
	recipe = uttl.buildout:vswhere
	version = latest

	[cmake]
	generator = Visual Studio ${visual-studio:version-tools} ${visual-studio:version-product} Win64