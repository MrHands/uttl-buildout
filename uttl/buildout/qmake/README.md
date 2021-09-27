# uttl.buildout.qmake

Generates project files using QMake. You must set the `vcvars` option if you intend to output project files for Visual Studio.

Qt makefiles use the `.pro` extension.

## Configuration 

`executable` (default: "qmake")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`inputs` (mandatory)

List of Qt makefiles used for generating project files.

`always-install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`template` (optional)

Overrides the `TEMPLATE` variable used in the makefiles.

`template-prefix` (optional)

Adds a prefix to the value of the `TEMPLATE` variable used in the makefiles.

`recursive` (optional)

Set this value to 1 to do a recursive search for linked makefiles while processing list of inputs.

`artefact-path` (optional)

Specifies the path to the expected output, used for tracking whether the script needs to run again.

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