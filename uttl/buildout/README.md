# uttl.buildout.command

Calls an executable with a list of arguments.

## Options 

`executable` (default: "cmd.exe")

Path to the executable used to run commands.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`artefacts` (optional)

List of files that will be installed by the recipe.

`arguments` (optional)

List of arguments that are added to the executable.

## Example - Generate a Visual Studio project using a custom codegen executable

	[generate-project-server]
	recipe = uttl.buildout:command
	executable = ${buildout:directory}/build/GenerateServer.exe
	source-dir = ${buildout:directory}/source/server
	arguments =
		--sourceDir
		${:source-dir}
	artefacts = ${:source-dir}/SSSG.vcxproj