# uttl.buildout.dotnet.restore

Uses NuGet to restore .NET packages on a Visual Studio project.

## Options

`executable` (default: "dotnet")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`project-path` (required)

Path to Visual Studio project file that will be processed.

`working-dir` (optional)

Change to this directory before executing the command.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`config-path` (optional)

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

`packages-dir` (optional)

Directory for restored packages.

`runtime` (optional)

Specifies a runtime for the package restore for packages not explicitly listed in the project file.

`source` (optional)

URI for the NuGet package source to use for the restore.

`use-lock-file` (optional)

Set this option to 1 to generate and use a lock file when restoring a project.

`verbosity` (optional)

Verbosity of logging output for the command. Must be one of `quiet`, `minimal`, `normal`, `detailed`, or `diagnostic`.

`artefacts` (optional)

Additional list of files that will be installed by the recipe but are not picked up automatically.

`arguments` (optional)

Additional list of arguments that are added to the executable _before_ the arguments generated by the recipe _without any processing_.

## Example - Restore packages for a C\# project

	[server-build-inkwrapper]
	recipe = uttl.buildout:dotnet-restore
	project-path = dependencies\InkWrapper\InkWrapper.csproj
