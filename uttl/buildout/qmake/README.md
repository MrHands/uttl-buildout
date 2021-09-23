# uttl.buildout.qmake

## Configuration 

`executable` (default: "qmake")

Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide `PATH` environment variable.

`files` (mandatory)

List of files

`always_install` (optional)

Set this option to 1 to skip checks for missing installed files and always run the script.

`template` (optional)

`template_prefix` (optional)

`recursive` (optional)

`artefact_path` (optional)

`warnings` (optional)

`vcvars` (optional)

none, all, parser, logic, deprecated

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
	template_prefix = vc
	recursive = 1
	artefact_path = ${qhttp-master:location}/qhttp.sln
	files = ${qhttp-master:location}/qhttp.pro