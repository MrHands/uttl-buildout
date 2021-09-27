import logging
import os
import re
import subprocess

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class QmakeRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='qmake')

		self.args = [ ]

		if 'template' in self.options:
			self.args += [ '-t', self.options['template'] ] 

		if 'template-prefix' in self.options:
			self.args += [ '-tp', self.options['template-prefix'] ]

		if 'recursive' in self.options:
			if self.options['recursive'] == '1':
				self.args += [ '-recursive' ]
			else:
				self.args += [ '-norecursive' ]

		if 'artefact-path' in self.options:
			self.args += [ '-o', self.options['artefact-path'] ]

		# warnings

		if 'warnings' in self.options:
			for w in self.options['warnings'].splitlines():
				if w in [ 'none', 'all', 'parser', 'logic', 'deprecated' ]:
					self.args += [ '-W%s' % (w) ]

		# inputs

		if not 'inputs' in self.options:
			raise UserError('Missing mandatory "inputs" parameter.')

		self.args += self.options['inputs'].splitlines()

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		self.options.created(self.options['artefact-path'])

		if 'vcvars' in self.options:
			prefix_args = [ self.options['vcvars'], 'amd64', '&&' ]
		else:
			prefix_args = []

		self.runCommand(self.args, prefixArgs=prefix_args, parseLine=self.parseLine)

		return self.options.created()

	check_errors = re.compile(r'.*ERROR:\s*(.*)')

	def parseLine(self, line):
		return not self.check_errors.match(line)

def uninstall(name, options):
	pass