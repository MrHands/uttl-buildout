# uttl.buildout.copyfile

Copies files from a source directory to a destination, both when the destination files do not exist and when the source files were modified.

## Configuration

`files` (required)

List of file names to copy from the source directory to the destination.

`source-path` (default: current working directory)

Directory where the source files are kept.

`destination-path` (default: current working directory)

Directory to copy the files to. Folder hierarchy will be created if it does not exist yet.

## Example - Copy source images to a media directory

	[buildout]
	parts = 
		copy-media

	[copy-media]
	recipe: uttl.buildout:copyfile
	source-path: source/art/backgrounds
	destination-path: build/media/backgrounds
	files:
		sky.jpg
		conveniencestore.jpg
		woods.jpg