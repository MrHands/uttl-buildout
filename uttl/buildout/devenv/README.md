# uttl.buildout.devenv

Invokes the Visual Studio development environment (`devenv.com`) to perform actions on projects and solutions.

This recipe will automatically track the resulting binary files, but it cannot check whether any of the input files have changed. Buildout will only call the recipe if the resulting binary files are missing. Visual Studio also tracks whether files have changed, so you can make sure that your binary files are always built by setting `always-install` in your options.

## Configuration Options

`executable` (default: "devenv.com")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`solution` (required)

Path to the Visual Studio solution file (.sln) that will be passed to the executable.

`project` (optional)

Project to run an action on, like `build`, `rebuild`, `clean`, or `deploy`. One of these actions must be specified for the `project` option to be considered valid.

`build` (optional)

Builds all projects in the solution if the parameter is left blank or builds a configuration for the selected project, e.g. `Release`.

`rebuild` (optional)

Rebuilds all projects in the solution if the parameter is left blank or rebuilds a configuration for the selected project, e.g. `Debug`.

`clean` (optional)

Cleans all projects in the solution if the parameter is left blank or cleans a configuration for the selected project, e.g. `ReleaseWithDebugInfo`.

`deploy` (optional)

Deploys all projects in  the solution if the parameter is left blank or deploys a configuration for the selected project, e.g. `Shipping`.

`command` (optional)

Starts Visual Studio and executes the specified command.

## Example - Build the game in Release

	[buildout]
	parts = 
		server-build-exe

	[server-build-exe]
	recipe = uttl.buildout:devenv
	executable = ${devenv:path}
	solution = SSSG.sln
	project = SSSG
	build = Release