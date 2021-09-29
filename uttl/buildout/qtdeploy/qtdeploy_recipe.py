import os.path
import re

from uttl.buildout.command_recipe import CommandRecipe
from zc.buildout import UserError

class QtDeployRecipe(CommandRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='windeployqt.exe')

		self.options.setdefault('target', 'release')

		# target

		if self.options['target'] == 'debug':
			self.args += [ '--debug' ]
			self.args += [ '--pdb' ]
		else:
			self.args += [ '--release' ]

		# translations

		if 'translations' in self.options:
			translations = self.options['translations'].splitlines()
			self.args += [ '--translations', ','.join(str(t) for t in translations) ]
		else:
			self.args += [ '--no-translations' ]

		# qml directory

		if 'qml-dir' in self.options:
			self.args += [ '--qmldir', os.path.abspath(self.options['qml-dir']) ]

		# qml import

		if 'qml-import' in self.options:
			self.args += [ '--qmlimport', os.path.abspath(self.options['qml-import']) ]

		# plugins

		if 'plugins' in self.options:
			self.args += [ '--no-plugins' ]

		# libraries

		if 'libraries' in self.options:
			self.args += [ '--no-libraries' ]

		# compiler runtime

		if 'compiler-runtime' in self.options:
			if self.options['compiler-runtime'] == '1':
				self.args += [ '--compiler-runtime' ]
			else:
				self.args += [ '--no-compiler-runtime' ]

		# webkit2

		if 'webkit2' in self.options:
			if self.options['webkit2'] == '1':
				self.args += [ '--webkit2' ]
			else:
				self.args += [ '--no-webkit2' ]

		# angle

		if 'angle' in self.options:
			if self.options['angle'] == '1':
				self.args += [ '--angle' ]
			else:
				self.args += [ '--no-angle' ]

		# software rasterizer

		if 'opengl-sw' in self.options:
			self.args += [ '--no-opengl-sw' ]

		# virtual keyboard

		if 'virtual-keyboard' in self.options:
			self.args += [ '--no-virtualkeyboard' ]

		# d3d

		if 'system-d3d-compiler' in self.options:
			self.args += [ '--no-system-d3d-compiler' ]

		# patch qt

		if 'patch-qt' in self.options:
			self.args += [ '--no-patchqt' ]

		# target path

		if not 'target-path' in self.options:
			raise UserError('Missing mandatory "target-path" parameter.')

		self.args += [ self.options['target-path'] ]

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		for a in self.artefacts:
			self.options.created(a)

		# build argument list

		if 'vcvars' in self.options:
			prefix_args = [ self.options['vcvars'], 'amd64', '&&' ]
		else:
			prefix_args = []

		# track files that will be installed

		self.files = []

		self.runCommand([ '--list', 'target' ] + self.args, prefixArgs=prefix_args, parseLine=self.parseFileList, quiet=True)

		for f in self.files:
			self.options.created(f)

		# copy files

		self.runCommand(self.args, prefixArgs=prefix_args)

		return self.options.created()

	def parseFileList(self, path):
		drive, tail = os.path.splitdrive(path)

		if drive != '':
			self.files += [ path ]

		return True

def uninstall(name, options):
	pass