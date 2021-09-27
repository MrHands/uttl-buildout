import os.path
import re

from uttl.buildout.install_recipe import InstallRecipe
from zc.buildout import UserError

class DevenvRecipe(InstallRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='devenv.com')

		if not 'solution' in self.options:
			raise UserError('Missing mandatory "solution" option.')

		self.args = [ os.path.abspath(self.options['solution']) ]

		if 'project' in self.options:
			self.args.extend([ '/Project', self.options['project'] ])

		if 'build' in self.options:
			self.args.extend([ '/Build', self.options['build'] ])

		if 'command' in self.options:
			self.args.extend([ '/Command', '"%s"' % self.options['command'] ])

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def install(self):
		self.runCommand(self.args, parseLine=self.parseLine)

		return self.options.created()

	check_errors = re.compile(r'.*Error: (.*)')
	check_failed = re.compile(r'.*(Build FAILED).*')
	check_artefacts = re.compile(r'.*(.+) -> (.+)')

	def parseLine(self, line):
		# check for errors

		if self.check_errors.match(line) or self.check_failed.match(line):
			return False

		# add artefacts to options

		match = self.check_artefacts.match(line)
		if match:
			self.options.created(match.group(2))

		return True

def uninstall(name, options):
	pass