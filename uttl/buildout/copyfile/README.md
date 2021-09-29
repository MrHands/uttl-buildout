# uttl.buildout.copyfile

Copies files from a source directory to a destination, both when the destination files do not exist and when the source files were modified.

## Configuration

`files` (required)

List of file names to copy from the source directory to the destination.

`source-dir` (default: current working directory)

Directory where the source files are kept.

`destination-dir` (default: current working directory)

Directory to copy the files to. Folder hierarchy will be created if it does not exist yet.

## Example - Copy source images to a media directory

	[copy-media]
	recipe: uttl.buildout:copyfile
	source-dir: ${buildout:directory}/source/art/backgrounds
	destination-dir: ${buildout:directory}/build/media/backgrounds
	files:
		sky.jpg
		conveniencestore.jpg
		woods.jpg