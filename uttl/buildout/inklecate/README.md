# uttl.buildout.inklecate

Calls the Inklecate compiler executable to compile .ink files into .json files.

## Configuration 

`executable` (default: "inklecate.exe")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`output-directory` (optional)

Directory where the  Defaults to the current directory.

`input` (mandatory)

List of .ink files to compile using Inklecate.

## Example - Build narrative source files to JSON using inklecate

	[buildout]
	parts = ink

	[ink]
	recipe = uttl.buildout:inklecate
	executable = C:\inklecate-0.9.0\inklecate.exe
	input =
		C:\Projects\SSSG\source\narrative\todo_mechanic.ink
		C:\Projects\SSSG\source\narrative\todo_diplomate.ink
		C:\Projects\SSSG\source\narrative\todo_amazon.ink
	output-directory = C:\Projects\SSSG\build\data\stories