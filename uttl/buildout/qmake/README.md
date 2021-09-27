# uttl.buildout.qmake

Generates project files from Qt makefiles (`.pro`) using QMake. You must set the `vcvars` option if you intend to output project files for Visual Studio.

Note that the recipe does not check whether the input files for QMake have changed, only if the output artefact is missing. Buildout will not install the recipe again if the files used by the makefile have changed. QMake also tracks whether inputs have changed, so you can use the `always-install` option if you want to make sure that the generated project files are always up to date.

## Configuration 

`executable` (default: "qmake")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`inputs` (mandatory)

List of Qt makefiles used for generating project files.

`artefact-path` (optional)

Specifies the path to the project file output. Also used for tracking whether the script needs to run again.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`template` (optional)

Overrides the `TEMPLATE` variable used in the makefiles.

`template-prefix` (optional)

Adds a prefix to the value of the `TEMPLATE` variable used in the makefiles. Setting this option to `vc` will tell QMake to output Visual Studio project files.

`recursive` (optional)

Set this value to 1 to do a recursive search for linked makefiles while processing the list of inputs.

`warnings` (optional)

List of warning levels to enable. Valid options are `none`, `all`, `parser`, `logic`, and `deprecated`.

`vcvars` (optional)

Path to `vcvarsall.bat` batch script that comes with Visual Studio. Must be set if you intend to output Visual Studio project files with QMake.

## Example

	[qhttp-master]
	<= git-clone
	repository = https://github.com/MrHands/qhttp.git

	[qhttp-dependency-http-parser]
	<= git-clone
	location = ${qhttp-master:location}/3rdparty/http-parser
	repository = https://github.com/nodejs/http-parser.git

	[qhttp-solution]
	=> qhttp-dependency-http-parser
	recipe = uttl.buildout:qmake
	executable = ${qmake:path}
	vcvars = ${vcvars:path}
	template-prefix = vc
	recursive = 1
	artefact-path = ${qhttp-master:location}/qhttp.sln
	files = ${qhttp-master:location}/qhttp.pro