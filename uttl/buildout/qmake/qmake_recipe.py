import re

from uttl.buildout.command_recipe import CommandRecipe
from zc.buildout import UserError

class QmakeRecipe(CommandRecipe):
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

		# warnings

		if 'warnings' in self.options:
			for w in self.options['warnings'].splitlines():
				if w in [ 'none', 'all', 'parser', 'logic', 'deprecated' ]:
					self.args += [ '-W%s' % (w) ]

		# artefact

		if not 'artefact-path' in self.options:
			raise UserError('Missing mandatory "artefact-path" option.')

		self.args += [ '-o', self.options['artefact-path'] ]

		# inputs

		if not 'inputs' in self.options:
			raise UserError('Missing mandatory "inputs" option.')

		self.args += self.options['inputs'].splitlines()

		self.args += self.additional_args

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		self.options.created(self.options['artefact-path'])

		for a in self.artefacts:
			self.options.created(os.path.abspath(a))

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