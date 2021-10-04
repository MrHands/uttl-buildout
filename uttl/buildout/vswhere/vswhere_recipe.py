import os
import re

from uttl.buildout.command_recipe import CommandRecipe
from zc.buildout import UserError

class VsVersionInfo:
	def __init__(self, product, dev):
		self.product = product
		self.dev = dev
		self.legacy = int(dev) <= 10
		self.use_env = int(dev) <= 9

class VsWhereRecipe(CommandRecipe):
	def __init__(self, buildout, name, options):
		super().__init__(buildout, name, options, executable=r'%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe')

		self.options.setdefault('display-name', '')
		self.options.setdefault('install-dir', '')
		self.options.setdefault('product-path', '')

		if not 'version' in self.options:
			raise UserError('Missing required "version" option.')

		version = self.options['version']
		versions_list = [
			VsVersionInfo('latest', '999'),
			VsVersionInfo('2019', '16'),
			VsVersionInfo('2017', '15'),
			VsVersionInfo('2015', '14'),
			VsVersionInfo('2013', '12'),
			VsVersionInfo('2012', '11'),
			VsVersionInfo('2010', '10'),
			VsVersionInfo('2008', '9'),
			VsVersionInfo('2005', '8'),
		]

		found = [v for v in versions_list if v.product == version or v.dev == version]
		if not found:
			raise UserError('Unhandled Visual Studio version "%s".' % (version))

		self.version = found[0]
		self.version_found = 0

		if self.version.use_env:
			self.options['args'] = ''

			env_var = 'VS' + self.version.dev + '0COMNTOOLS'
			if not env_var in os.environ:
				raise UserError('Could not find path to Visual Studio %s.' % (self.version.product))

			self.version_found = int(self.version.dev)

			self.options['display-name'] = 'Visual Studio %s' % (self.version.product)

			tools_dir = os.environ[env_var]
			install_dir = os.path.abspath(os.path.join(tools_dir, '../../'))

			self.options['install-dir'] = install_dir
			self.options['product-path'] = os.path.join(install_dir, 'Common7\\IDE\\VCExpress.exe')
			self.options['vcvars-path'] = os.path.join(install_dir, 'VC\\vcvarsall.bat')
		else:
			if self.version.product == 'latest':
				self.args += [ '-latest' ]
			else:
				if self.version.legacy:
					self.args += [ '-legacy' ]

				self.args += [ '-version', self.version.dev ]

			self.options['args'] = ' '.join(str(e) for e in self.args)

			self.runCommand(self.args, parseLine=self.parseLine, quiet=True)

			self.options['vcvars-path'] = os.path.join(self.options['install-dir'], 'VC\\Auxiliary\\Build\\vcvarsall.bat')

		if self.version_found < int(self.version.dev):
			raise UserError('Visual Studio %s was not found.' % (self.version.product))

		if not os.path.exists(self.options['vcvars-path']):
			raise UserError('Failed to retrieve path to "vcvarsall.bat" script.')

	def command_install(self):
		pass

	_property = re.compile(r'\s*(\w+)\: (.+)').match
	_semantic_version = re.compile(r'(\d+)\.(\d+).(\d+)\+(\d+)\.(\d+)$').match

	def parseLine(self, line):
		self.log.debug(line)

		match = self._property(line)
		if match:
			name = match.group(1)
			value = match.group(2)

			if name == 'installationPath':
				self.options['install-dir'] = value
			elif name == 'productPath':
				self.options['product-path'] = value
			elif name == 'displayName':
				self.options['display-name'] = value
			elif name == 'catalog_productSemanticVersion':
				self.version_found = int(self._semantic_version(value).group(1))

		return True

def uninstall(name, options):
	pass