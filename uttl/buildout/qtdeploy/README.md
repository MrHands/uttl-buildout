# uttl.buildout.qtdeploy

## Configuration 

``target_path`` (mandatory)

  Path to the executable that the Qt deployment tool will inspect for dependencies.

``always_build`` (optional)

  Set this option to 1 to skip checks for missing installed files and always run the script.

``executable`` (default: "windeployqt.exe")

  Path to the executable used to run commands. You don't need to set this if the executable was added to the system-wide ``PATH`` environment variable.

``target`` (default: release)

  Deploy either ``debug`` or ``release`` versions of Qt libraries. The debug target will also deploy .pdb files which are used when debugging using Visual Studio.

``vcvars`` (optional)

  Path to ``vcvarsall.bat``, a script file used to determine the install path of Visual Studio. Only required if you want to deploy the Visual Runtime C++ installer.

``translations`` (optional)

  List of translated languages to deploy, e.g. fr, uk, de. Leaving this option unspecified will skip deployment of translations.

``compiler_runtime`` (optional)

  Force deployment of compiler runtime libraries by setting this option to 1. Disable deployment by setting it to 0.

``webkit2`` (optional)

  Force deployment of WebKit2 libraries by setting this option to 1. Disable deployment by setting it to 0.

``angle`` (optional

  Force deployment of ANGLE libraries by setting this option to 1. Disable deployment by setting it to 0.

``opengl_sw`` (default: 1)

  Disable deployment of the OpenGL software rasterizer library by setting this option to 0.

``virtual_keyboard`` (default: 1)

  Disable deployment of the Virtual Keyboard libraries by setting this option to 0.

``system_d3d_compiler`` (default: 1)

  Disable deployment of the system Direct3D compiler libraries by setting this option to 0.

## Example

	[buildout]
	parts = deploy

	[deploy]
	recipe = uttl.buildout:qtdeploy
	executable = C:\Qt\5.15.2\msvc2019_64\bin\windeployqt.exe
	translations =
		uk
		de
		fr
	target_path = C:\Projects\SSSG\build\SSSGRelease.exe