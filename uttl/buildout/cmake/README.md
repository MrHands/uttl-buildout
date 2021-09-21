# uttl.buildout.cmake

Executes commands using a CMake build script, to e.g. to generate a Visual Studio solution or build an executable.

The recipe will automatically keep track of files that were generated, including when you run an `INSTALL` target. Only when the output was deleted will the command be run again.

## Configuration Options

``always_build`` (optional)

  Set this option to 1 to skip checks for missing installed files and always run the script.

``executable`` (default: "cmake")

  Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide ``PATH`` environment variable.

``artefact_path`` (optional)

  Manual tracking for the path to the artefact generated by CMake. While the script will automatically parse the output and track files that were generated, this option can be useful to ensure that commands are run again when the output was deleted.

``generator`` (optional)

  Specifies the generator used by CMake when configuring the build environment, e.g. ``Visual Studio 2017 15 Win64``.

``configure_path`` (optional)

  Path for the output of the CMake configure step. When you are e.g. generating a Visual Studio solution then this is the path where it will be generated to. If the path is not specified it will default to the ``build_path``.

``build_path`` (optional)

  Builds the ``CMakeList.txt`` project at the specified path.

``install_path`` (optional)

  Synonym for ``build_path`` with the caveat that it will also set the variable ``CMAKE_INSTALL_PREFIX`` to this path.

``target`` (optional)

  Target(s) to build from the generated environment using the specified generator.

``config`` (optional)

  Configuration to build from the generated environment using the specified generator.

## Example

Downloads the SDL2 library and builds a release DLL for Windows using Visual Studio 2017.

	[buildout]
	parts = 
		sdl-download
		sdl-build

	[sdl-download]
	recipe = hexagonit.recipe.download
	version = 2.0.16
	url = https://www.libsdl.org/release/SDL2-${:version}.zip
	strip-top-level-dir = true
	destination = ${buildout:parts-directory}/sdl-download

	[sdl-solution]
	recipe = uttl.buildout:cmake
	build_path = ${sdl-download:destination}
	configure_path = ${sdl-download:destination}/build
	install_path = ${sdl-download:destination}
	artefact_path = ${:configure_path}/SDL2.sln
	generator = Visual Studio 15 2017 Win64

	[sdl-build]
	recipe = uttl.buildout:cmake
	build_path = ${sdl-solution:configure_path}
	target = install
	config = Release