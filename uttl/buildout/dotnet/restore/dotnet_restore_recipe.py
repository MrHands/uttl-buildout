import os.path
import re

from uttl.buildout.dotnet.dotnet_recipe import DotnetRecipe
from zc.buildout import UserError

class DotnetRestoreRecipe(DotnetRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options)

		# dotnet restore [<ROOT>] [--configfile <FILE>] [--disable-parallel]
		#	[-f|--force] [--force-evaluate] [--ignore-failed-sources]
		#	[--interactive] [--lock-file-path <LOCK_FILE_PATH>] [--locked-mode]
		#	[--no-cache] [--no-dependencies] [--packages <PACKAGES_DIRECTORY>]
		#	[-r|--runtime <RUNTIME_IDENTIFIER>] [-s|--source <SOURCE>]
		#	[--use-lock-file] [-v|--verbosity <LEVEL>]

		self.args += [ 'restore' ]

		for i in self.inputs:
			self.args.append(os.path.abspath(i))

		if 'config-file' in self.options:
			self.args += [ '--configfile', os.path.abspath(self.options['config-file']) ]

		if 'parallel' in self.options and self.options['parallel'] == '0':
			self.args += [ '--disable-parallel' ]

		if 'force' in self.options:
			self.args += [ '--force' ]

		if 'force-evaluate' in self.options:
			self.args += [ '--force-evaluate' ]

		if 'ignore-failed-sources' in self.options:
			self.args += [ '--ignore-failed-sources' ]

		if 'interactive' in self.options:
			self.args += [ '--interactive' ]

		if 'locked-mode' in self.options:
			self.args += [ '--locked-mode' ]

		if 'no-cache' in self.options:
			self.args += [ '--no-cache' ]

		if 'no-dependencies' in self.options:
			self.args += [ '--no-dependencies' ]

		if 'packages-path' in self.options:
			self.args += [ '--packages', os.path.abspath(self.options['packages-path']) ]

		if 'runtime' in self.options:
			self.args += [ '--runtime', self.options['runtime'] ]

		if 'source' in self.options:
			self.args += [ '--source', self.options['source'] ]

		if 'use-lock-file' in self.options:
			self.args += [ '--use-lock-file' ]

		if 'verbosity' in self.options:
			self.args += [ '--verbosity', self.options['verbosity'] ]

		self.options['args'] = ' '.join(str(e) for e in self.args)

def uninstall(name, options):
	pass