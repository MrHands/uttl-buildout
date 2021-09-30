# Changes

## 1.2.1 - 2021-09-30

* Command: Added missing `always-install` option to documentation
* Command: Added `working-dir` option
* CopyFile: Renamed `source-path`, `destination-path` to `-dir` (old names treated as synonymous)
* CMake: Renamed `source-path`, `install-path`, `configure-path`, and `build-path` to `-dir` (old names treated as synonymous)
* CMake: Added `working-dir` option
* DotnetRestore: Fixed recipe being registered with the wrong name
* DotnetRestore: Renamed `config-file` to `config-path` (old name treated as synonymous)
* DotnetRestore: Renamed `packages-path` to `packages-dir` (old name treated as synonymous)
* DotnetRestore: Added `working-dir` option
* Devenv: Renamed `solution` to `solution-path` (old name treated as synonymous)
* Devenv: Added `working-dir` option
* Inklecate: Renamed `output-directory` to `output-dir` (old name treated as synonymous)
* Inklecate: Renamed `input` to `inputs` (old name treated as synonymous)
* Inklecate: Added `working-dir` option
* QMake: Added `working-dir` option
* QtDeploy: Added `dir`, `libraries-dir`, `plugins-dir`, `libraries`, `qml-dir`, `qml-import`, `plugins`, and `patch-qt` options
* QtDeploy: Added `lib-` option to explicity add or skip libaries
* QtDeploy: Added `working-dir` option
* VersionCheck: Made `body` option mandatory


## 1.2.0 - 2021-09-28

* All: Added optional artefacts and arguments options
* CMake: Made the path to source option mandatory to prevent user error
* Command: New recipe for calling executables
* CopyFile: Install files before copying them

## 1.1.0 - 2021-09-27

* All: Changed all options from snake_case to kebab-case
* DotnetRestore: New recipe for invoking dotnet commands
* CMake: Fixed source path option
* CMake: Made target option a synonym for targets
* CopyFile: Copies files if they do not exist or if they were modified
* CopyFile: Added documentation
* Devenv: Cleaned up script
* Devenv: Added documentation
* QMake: Fixed files option throwing an error
* QMake: Expanded documentation
* QMake: Fixed typos in documentation

## 1.0.0 - 2021-09-26

* Initial release