# uttl.buildout.dotnet.restore

Uses NuGet to restore .NET packages on a Visual Studio project.

## Configuration

`inputs` (required)

`executable` (default: "cmake")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`config-file` (optional)

`parallel` (optional)

Set this value to 0 to disable restore multiple projects in parallel.

`force` (optional)

`force-evaluate` (optional)

`ignore-failed-sources` (optional)

`interactive` (optional)

`locked-mode` (optional)

`cache` (optional)

Set this value to 0 to disable caching HTTP requests.

`dependencies` (optional)

Set this value to 0 to only restore the root project and not any of the project it references.

`packages-path` (optional)

Directory for restored packages.

`runtime` (optional)

`source` (optional)

`use-lock-file` (optional)

`verbosity` (optional)

## Example - Restore packages for a C\# project

	[server-build-inkwrapper]
	recipe = uttl.buildout:dotnet.restore
	inputs = dependencies\InkWrapper\InkWrapper.csproj
