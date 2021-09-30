import os.path
import re

from uttl.buildout.command_recipe import CommandRecipe
from zc.buildout import UserError

class VsWhereRecipe(CommandRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable=r'%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe')

		if 'version' in self.options:
			version = self.options['version']
			versions_map = {
				'latest': {
					'dev': 'latest',
					'legacy': False
				},
				'2019': {
					'dev': '16',
					'legacy': False
				},
				'2017': {
					'dev': '15',
					'legacy': False
				},
				'2015': {
					'dev': '14',
					'legacy': False
				},
				'2013': {
					'dev': '12',
					'legacy': False
				},
				'2012': {
					'dev': '11',
					'legacy': False
				},
				'2010': {
					'dev': '10',
					'legacy': True
				},
				'2008': {
					'dev': '9',
					'legacy': True
				},
				'2005': {
					'dev': '8',
					'legacy': True
				},
			}
			if not version in versions_map:
				raise UserError('Unhandled Visual Studio version "%s".' % (version))

			self.version = versions_map[version]

			if self.version['dev'] == 'latest':
				self.args += [ '-latest' ]
			else:
				if self.version['legacy']:
					self.args += [ '-legacy' ]

				self.args += [ '-version', self.version['dev'] ]

		if 'latest' in self.options:
			self.args += [ '-latest' ]

		if 'get-install-path' in self.options:
			self.args += [ '-property', 'installationPath' ]

		# set pre=Microsoft.VisualStudio.Product.
		# set ids=%pre%Community %pre%Professional %pre%Enterprise %pre%BuildTools

		if 'products' in self.options:
			self.args.append('-products')

			products = self.options['products'].splitlines()
			for p in products:
				self.args.append('Microsoft.VisualStudio.Product.' + p)

		# combine arguments

		self.options['args'] = ' '.join(str(e) for e in self.args)

	def command_install(self):
		self.runCommand(self.args, parseLine=self.parseLine)

	check_errors = re.compile(r'.*ERROR:\s*(.*)')

	def parseLine(self, line):
		return not self.check_errors.match(line)

def uninstall(name, options):
	pass