import os.path
import re

from uttl.buildout.command_recipe import CommandRecipe
from zc.buildout import UserError

class VsWhereRecipe(CommandRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable='vswhere.exe')

		# combine arguments

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def command_install(self):
		self.runCommand(self.args, parseLine=self.parseLine)

	check_errors = re.compile(r'.*ERROR:\s*(.*)')

	def parseLine(self, line):
		return not self.check_errors.match(line)

def uninstall(name, options):
	pass