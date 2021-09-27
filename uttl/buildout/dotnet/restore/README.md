# uttl.buildout.dotnet.restore

Uses NuGet to restore .NET packages on a Visual Studio project.

## Configuration

`inputs` (required)

List of project files to process.

`executable` (default: "cmake")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`config-file` (optional)

Path to a configuration file for NuGet to use. Only the settings from this file will be used if this option is specified.

`parallel` (optional)

Set this option to 0 to disable restore multiple projects in parallel.

`force` (optional)

Set this option to 1 to resolve all dependencies even if the last restore was succesful.

`force-evaluate` (optional)

Set this option to 1 to reevaluate all dependencies even if a lock file already exists.

`ignore-failed-sources` (optional)

Set this option to 1 to output a warning if a package fails to meet the version requirements.

`interactive` (optional)

Set this option to 1 to allow the command to stop and wait for user input, e.g. authentication.

`lock-file-path` (optional)

Path for the project lock file.

`locked-mode` (optional)

Set this option to 0 to disable updating the project lock file.

`cache` (optional)

Set this option to 0 to disable caching HTTP requests.

`dependencies` (optional)

Set this option to 0 to only restore the root project and not any of the project it references.

`packages-path` (optional)

Directory for restored packages.

`runtime` (optional)

Specifies a runtime for the package restore for packages not explicitly listed in the project file.

`source` (optional)

URI for the NuGet package source to use for the restore.

`use-lock-file` (optional)

Set this option to 1 to generate and use a lock file when restoring a project.

`verbosity` (optional)

Verbosity of logging output for the command. Must be one of `quiet`, `minimal`, `normal`, `detailed`, or `diagnostic`.

## Example - Restore packages for a C\# project

	[server-build-inkwrapper]
	recipe = uttl.buildout:dotnet.restore
	inputs = dependencies\InkWrapper\InkWrapper.csproj
