# uttl.buildout.vswhere

Recipe for retrieving the installation path to Visual Studio using Microsoft's `vswhere` tool.

## Options

`executable` (default: "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe")

Path to the executable used to run commands. While the executable should always be available after installing a new version of Visual Studio, you can still opt to use a version that is installed locally.

`version` (required)

Version of Visual Studio that you want to retrieve. Can be a product number (e.g. 2017), a tools number (e.g. 10), or "latest". An error will be raised if the requested version could not be found.

`latest` (optional)

`install-path` (optional)

`products` (optional)

## Outputs

## Example

	[visual-studio]
	recipe = uttl.buildout:vswhere